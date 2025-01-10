from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Shop
from .serializers import ShopSerializer


# 1. Create a new shop (or retrieve an existing one)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_shop(request):
    # If the user already has a shop, return an error
    if Shop.objects.filter(owner=request.user).exists():
        return Response({'error': 'You already have a shop.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create a new shop instance with the logged-in user as the owner
    data = request.data
    data['owner'] = request.user.id 

    serializer = ShopSerializer(data=data)
    if serializer.is_valid():
        shop = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. Get the shop profile for the logged-in user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_shop(request):
    try:
        shop = Shop.objects.get(owner=request.user)
        serializer = ShopSerializer(shop)
        return Response(serializer.data)
    except Shop.DoesNotExist:
        return Response({"error": "Shop not found."}, status=status.HTTP_404_NOT_FOUND)


# 3. Update the shop profile (partially or fully)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_shop(request):
    try:
        shop = Shop.objects.get(owner=request.user)
        serializer = ShopSerializer(shop, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Shop.DoesNotExist:
        return Response({"error": "Shop not found."}, status=status.HTTP_404_NOT_FOUND)


# 4. Delete the shop profile
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_shop(request):
    try:
        shop = Shop.objects.get(owner=request.user)
        shop.delete()
        return Response({"message": "Shop deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Shop.DoesNotExist:
        return Response({"error": "Shop not found."}, status=status.HTTP_404_NOT_FOUND)
