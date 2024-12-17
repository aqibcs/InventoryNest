from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail

from InventoryNest import settings
from .models import Order
from .serializers import OrderSerializer
from products.models import Product


# Create an order (public access - for both authenticated and unauthenticated users)
@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    data = request.data

    # If the user is authenticated, use their user ID
    if request.user.is_authenticated:
        data['user'] = request.user.id
    else:
        # If the user is not authenticated, we require a guest email
        guest_email = data.get('guest_email')
        if not guest_email:
            return Response(
                {"error": "Guest email is required for anonymous orders."},
                status=status.HTTP_400_BAD_REQUEST)
        data['guest_email'] = guest_email  # Set the guest email

    # Validate if enough stock is available before saving
    product_id = data.get('product')
    quantity = data.get('quantity')

    try:
        product = Product.objects.get(id=product_id)
        if product.stock < quantity:
            return Response({"error": "Not enough stock available."},
                            status=status.HTTP_400_BAD_REQUEST)
    except Product.DoesNotExist:
        return Response({"error": "Product not found."},
                        status=status.HTTP_404_NOT_FOUND)

    # Serialize the data and save the order
    serializer = OrderSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        # Reduce stock of the product once the order is successfully created
        product.stock -= quantity
        product.save()

        # Send order confirmation email
        user_email = data.get(
            'guest_email'
        ) if not request.user.is_authenticated else request.user.email
        try:
            send_mail(
                subject="Order Confirmation from InventoryNest",
                message=(
                    f"Hi {user_email},\n\nYour order for {product.name} has been successfully placed! We'll notify you when your order status is updated.\n\nThank you for shopping with us!"),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user_email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email: {e}")

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# List all orders (GET request) (Admin only or authenticated users if needed)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Retrieve a single order (GET request)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'error': "Order not found."},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_order(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response({'error': "Order not found."},
                        status=status.HTTP_404_NOT_FOUND)

    # Ensure the user has the correct permissions
    if not (request.user == order.user or request.user.is_staff):
        return Response(
            {"error": "You don't have permission to update this order."},
            status=status.HTTP_403_FORBIDDEN)

    serializer = OrderSerializer(order, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        # Save the updated order
        serializer.save()

        # Notify user about the status update if applicable
        if 'status' in request.data:
            status_message = request.data['status']

            # Determine the user's email
            user_email = order.user.email if order.user else order.guest_email

            if user_email:
                try:
                    # Send email notification about the status update
                    send_mail(
                        subject="Your Order Status Update",
                        message=(f"Hi {user_email},\n\n"
                                 f"Your order for {order.product.name} has been updated to: {status_message}.\n\n"
                                 "Thank you for shopping with us!"),
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[user_email],
                        fail_silently=False,
                    )
                except Exception as e:
                    # Log email errors for debugging
                    print(f"Error sending email: {e}")

        # Save the updated order
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# Delete order (DELETE request)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'error': "Order not found."},
                        status=status.HTTP_404_NOT_FOUND)

    # Add stock back to product when an order is deleted
    product = order.product
    product.stock += order.quantity
    product.save()

    # Notify the customer that the order was canceled
    try:
        send_mail(
            subject="Your Order Has Been Canceled",
            message=
            (f"Hi {order.user.email},\n\n"
            f"We're sorry to inform you that your order for '{order.product.name}' has been canceled due to unforeseen circumstances.\n"
            f"Reason: Operational challenges.\n\n"
            "If you have any questions or concerns, please feel free to contact our support team.\n\n"
            "Thank you for your patience and understanding.\n\n"
            "Best regards,\nThe InventoryNest Team."),
            recipient_list=[order.user.email],
            fail_silently=False,
        )
    except Exception as e:
            print(f"Error sending email: {e}")

    order.delete()
    return Response({"message": "Order deleted successfully."},
                    status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_order(request, pk):
    """
    Allow users to cancel their own orders.
    """
    try:
        # Retrieve the order
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'error': "Order not found."},
                        status=status.HTTP_404_NOT_FOUND)

    # Ensure the user owns the order
    if order.user != request.user:
        return Response(
            {"error": "You do not have permission to cancel this order."},
            status=status.HTTP_403_FORBIDDEN)

    # Send an email notification to the product owner
    try:
        send_mail(
            subject="Order Canceled by User",
            message=
            (f"Hi {order.product.user.email},\n\n"
            f"The user {order.user.username} has canceled their order for '{order.product.name}'.\n"
            "If you have already started processing this order, please contact the user for clarification.\n\n"
            "Thank you for your understanding.\n\n"
            "Best regards,\nThe InventoryNest Team."),
            recipient_list=[order.product.user.email],  # Notify the product owner
            fail_silently=False,
        )
    except Exception as e:
            print(f"Error sending email: {e}")

    # Send a confirmation email to the user
    try:
        send_mail(
            subject="Your Order Has Been Canceled",
            message=
            (f"Hi {order.user.email},\n\n"
            f"You have successfully canceled your order for '{order.product.name}'.\n"
            "If this was a mistake or you need further assistance, please contact our support team.\n\n"
            "Thank you for using our service.\n\n"
            "Best regards,\nThe InventoryNest Team."),
            recipient_list=[order.user.email],
            fail_silently=False,
        )
    except Exception as e:
            print(f"Error sending email: {e}")

    # Delete the order
    order.delete()

    return Response(
        {
            "message":
            "Order canceled successfully. Notifications have been sent."
        },
        status=status.HTTP_200_OK)
