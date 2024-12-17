import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated

from InventoryNest import settings
from users.models import UserProfile
from .forms import *
from .serializers import UserProfileSerializer
from django.core.mail import send_mail
from .utils import generate_otp
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from django.db.models import Q


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
        user = user_form.save(commit=False)
        user.is_active = False  # Account is inactive until verified
        user.save()

        # Create UserProfile with default values (null for optional fields)
        UserProfile.objects.create(user=user,
                                address=None, payment_info=None, preferences=None)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verification_link = f"{request.build_absolute_uri('/verify-email/')}{uid}/{token}/"

        # Send a verification email
        try:
            send_mail(
                subject="Verify Your Email",
                message=
                f"Click the link to verify your account: {verification_link}",
                recipient_list=[user.email],
                from_email=settings.EMAIL_HOST_USER,
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email: {e}")

        return Response(
            {"message": "Account created. Please verify your email."},
            status=status.HTTP_201_CREATED)
    return Response(user_form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request, uid, token):
    """
    Verify the user's email using the provided token and UID
    """
    try:
        user_id = force_bytes(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully!"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid token."},
                            status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response({"error": "Email verification failed."},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Authenticate user with either email or username and password, 
    then send an OTP to their email upon successful authentication.
    """
    login_form = UserLoginForm(data=request.data)
    if not login_form.is_valid():
        return Response(login_form.errors, status=status.HTTP_400_BAD_REQUEST)

    identifier = login_form.cleaned_data['identifier']
    password = login_form.cleaned_data['password']

    # Check whether the identifier is an email or username
    user = User.objects.filter(Q(email=identifier) | Q(username=identifier)).first()

    # Check if user exists and credentials are correct
    if user is None or not user.check_password(password):
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    # Check if the email is verified (is_active)
    if not user.is_active:
        return Response(
            {"error": "Email not verified. Please verify your email before logging in."},
            status=status.HTTP_403_FORBIDDEN
        )

    # Generate OTP if email is verified
    otp = generate_otp()

    # Store OTP in cache (keyed by identifier)
    cache_key = f"otp_{identifier}"
    cache.set(cache_key, otp, timeout=300)

    # Send OTP via email
    try:
        send_mail(
            subject="Your OTP for Login",
            message=(f"Dear {user.username},\n\n"
                     f"Your OTP for login is: {otp}\n\n"
                     f"Best Regards,\nInventoryNest Team"),
            recipient_list=[user.email],
            from_email=settings.EMAIL_HOST_USER,
            fail_silently=False,
        )
    except Exception as e:
        logging.error(f"Failed to send OTP to {user.email}: {e}")
        return Response(
            {"error": "Failed to send OTP. Please try again later."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response(
        {"message": "OTP sent to your email."},
        status=status.HTTP_200_OK,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    """
    Verify the OTP sent to the user's email and log the user in upon success.
    """
    identifier = request.data.get('identifier')
    otp = request.data.get('otp')

    if not identifier or not otp:
        return Response({"error": "Identifier and OTP are required."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Retrieve OTP from cache (keyed by identifier)
    cache_key = f"otp_{identifier}"
    cached_otp = cache.get(cache_key)

    if cached_otp is None:
        return Response(
            {"error": "OTP has expired. Please request a new one."},
            status=status.HTTP_401_UNAUTHORIZED)

    if cached_otp != otp:
        return Response({"error": "Invalid OTP."},
                        status=status.HTTP_401_UNAUTHORIZED)

    # Authenticate user by identifier (email or username)
    user = User.objects.filter(Q(email=identifier)
                               | Q(username=identifier)).first()
    if user is None:
        return Response({"error": "User does not exist."},
                        status=status.HTTP_404_NOT_FOUND)

    # Issue JWT tokens
    token = get_tokens_for_user(user)

    # Clear OTP after successful verification
    cache.delete(cache_key)

    return Response(
        {
            "message": "Login successful.",
            "token": token,
        },
        status=status.HTTP_200_OK,
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_profile(request):
    """
    Retrieve the authenticated user's profile details.
    """
    user = request.user

    try:
        user_profile, created = UserProfile.objects.get_or_create(user=user)
    except Exception as e:
        return Response(
            {"error": f"Failed to retrieve or create profile: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    serializer = UserProfileSerializer(user_profile)
    response_data = serializer.data
    if created:
        response_data["message"] = "Profile was newly created."
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update the authenticated user's profile details.
    """
    user = request.user

    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return Response(
            {"error": "User profile does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "Profile updated successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK,
        )
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
        {
            "message":
            "Your account has been deleted. We're sorry to see you go."
        },
        status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Logout the user by blacklisting their refresh token.
    """
    try:
        # Extract the refresh token from the request
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token is required for logout."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Blacklist the refresh token
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({"message": "User logged out successfully."},
                        status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": f"An error occurred during logout: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
