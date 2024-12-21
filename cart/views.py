from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer
from products.models import Product
from orders.models import Order


@api_view(['POST'])
@permission_classes([AllowAny])
def add_to_cart(request):
    # Use session ID if the user is unauthenticated
    user = request.user if request.user.is_authenticated else None
    session_id = request.session.session_key

    # Ensure the session is valid
    if not session_id:
        request.session.create()

    data = request.data
    serializer = CartItemSerializer(data=data)

    if serializer.is_valid():
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        # Get or create a cart for the user or session
        cart, created = Cart.objects.get_or_create(user=user, session_id=session_id)

        # Check if the item already exists in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        cart_item.save()

        return Response({
            "message": "Item added to cart."
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])  # Allow access to both authenticated and unauthenticated users
def view_cart(request):
    # Use session ID if the user is unauthenticated
    user = request.user if request.user.is_authenticated else None
    session_id = request.session.session_key

    # Ensure the session is valid for unauthenticated users
    if not session_id:
        request.session.create()

    try:
        # Get the cart using either user or session_id
        cart = Cart.objects.get(user=user, session_id=session_id)
    except Cart.DoesNotExist:
        return Response({"message": "Your cart is empty."}, status=status.HTTP_200_OK)

    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_cart(request):
    user = request.user
    product_id = request.data.get('product')
    new_quantity = request.data.get('quantity')

    if not product_id or not isinstance(product_id, int):
        return Response({'error': 'Invalid product ID.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cart = Cart.objects.get(user=user)
        cart_item = cart.items.get(product__id=product_id)
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        return Response({'error': 'Item not found in cart.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CartItemSerializer(cart_item, data={'quantity': new_quantity, 'product': product_id}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Cart item updated.'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    user = request.user
    product_id = request.data.get('product')

    try:
        cart = Cart.objects.get(user=user)
        cart_item = cart.items.get(product__id=product_id)
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        return Response({'error': 'Item not found in cart.'}, status=status.HTTP_404_NOT_FOUND)

    cart_item.delete()
    return Response({'message': 'Item removed from cart.'}, status=status.HTTP_200_OK)
