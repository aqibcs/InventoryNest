from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from .forms import *
from django.contrib.auth import authenticate
from .serializers import UserProfileSerializer
from django.core.mail import send_mail


# Function for generate a JWT token for user
def get_tokens_for_user(user):
    token = RefreshToken.for_user(user)
    return {'refresh': str(token), 'access': str(token.access_token)}


# Function to signin a user
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    user_form = UserRegistrationForm(data=request.data)
    if user_form.is_valid():
        user = user_form.save()

        # Generate token
        token = get_tokens_for_user(user)

        # Send a success email
        try:
            send_mail(
                subject="Welcome to InventoryNest!",
                message=
                f"Hi {user.username},\n\nThank you for signing up! We're excited to have you on board.\n\n"
                "Best regards,\n\nThe InventoryNest Team",
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email: {e}")

        return Response(
            {
                "message": "User registered successfully.",
                "token": token
            },
            status=status.HTTP_201_CREATED)
    return Response(user_form.errors, status=status.HTTP_400_BAD_REQUEST)


# Function to login a user
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    login_form = UserLoginForm(data=request.data)
    if login_form.is_valid():
        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                # Generate a token
                token = get_tokens_for_user(user)
                return Response(
                    {
                        "message": "User login successfully.",
                        "token": token
                    },
                    status=status.HTTP_200_OK)
            else:
                return Response({"error": "user ia inactive"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "Invalid credential."},
                            status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(login_form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """
    Retrieve the profile of the authenticated user.
    """
    try:
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except:
        return Response("An error occurred while retrieving the profile.",
                        status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update the profile of the authenticated user (partial updates).
    """
    user = request.user
    serializer = UserProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "Profile updated successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    """
    Deletes the authenticated user's account and sends a goodbye email.
    """
    user = request.user

    # Send the 'Sorry to see you leave' email
    send_mail(
        subject='Sorry to See You Go',
        message=f"Dear {user.name},\n\n"
        "We’re sorry to see you go. Thank you for being a part of our journey. "
        "If there’s anything we could improve, we’d love to hear your feedback.\n\n"
        "Best wishes,\nThe InventoryNest Team",
        recipient_list=[user.email],
        fail_silently=False,
    )

    # Delete the user account
    user.delete()

    return Response(
        {"message": "Your account has been deleted. We're sorry to see you go."},
        status=status.HTTP_200_OK
    )
