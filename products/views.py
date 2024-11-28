from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Product
from .serializers import ProductsSerializer


# 1. Create Product (POST request)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    serializer = ProductsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. List Products (GET request) with Pagination
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_products(request):
    products = Product.objects.filter(user=request.user)

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
    paginator.page_size = 10  # Default page size, you can adjust as needed
    paginated_products = paginator.paginate_queryset(products, request)

    serializer = ProductsSerializer(paginated_products, many=True)
    return paginator.get_paginated_response(serializer.data)


# 3. Retrieve Single Product (GET request)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product(request, pk):
    try:
        product = Product.objects.get(pk=pk, user=request.user)
    except Product.DoesNotExist:
        return Response({'error': "Product not found."},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = ProductsSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 4. Update Product (PUT/PATCH request)
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


# 5. Delete Product (DELETE request)
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
