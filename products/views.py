from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Product
from .serializers import ProductsSerializer
from shop.models import Shop


# 1. Create Product (POST request) - Only for users who have a shop
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    # Check if the user has a shop
    try:
        shop = Shop.objects.get(owner=request.user)
    except Shop.DoesNotExist:
        return Response({"error": "You must create a shop before uploading products."},
                        status=status.HTTP_400_BAD_REQUEST)

    # If the user has a shop, allow them to upload a product
    serializer = ProductsSerializer(data=request.data)
    if serializer.is_valid():
        # Set the user who is uploading the product
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. List Products (GET request) with Pagination - Anyone can view products
@api_view(['GET'])
@permission_classes([AllowAny])
def list_products(request):
    products = Product.objects.all()

    # Apply search filter (e.g., search by product name)
    search_query = request.query_params.get('search', '')
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Apply ordering (e.g., order by creation date or price)
    ordering = request.query_params.get('ordering', 'created_at')
    allowed_ordering = ['created_at', 'price', '-created_at', '-price']
    if ordering in allowed_ordering:
        products = products.order_by(ordering)

    # Pagination
    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_products = paginator.paginate_queryset(products, request)

    serializer = ProductsSerializer(paginated_products, many=True)
    return paginator.get_paginated_response(serializer.data)


# 3. Retrieve Single Product (GET request) - Any user can view a product
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': "Product not found."},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = ProductsSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 4. Update Product (PUT/PATCH request) - Only the product owner (user) can update it
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    try:
        product = Product.objects.get(pk=pk, user=request.user)
    except Product.DoesNotExist:
        return Response({'error': "Product not found."},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = ProductsSerializer(product, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 5. Delete Product (DELETE request) - Only the product owner (user) can delete it
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk, user=request.user)
    except Product.DoesNotExist:
        return Response({'error': "Product not found."},
                        status=status.HTTP_404_NOT_FOUND)

    product.delete()
    return Response({"message": "Product deleted successfully."},
                    status=status.HTTP_204_NO_CONTENT)
