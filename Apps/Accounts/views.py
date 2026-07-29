from . import firebase
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
)
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from firebase_admin import auth as firebase_auth
from django.contrib.auth import get_user_model
from Apps.Profile.models import UserProfile

User = get_user_model()


class RegisterView(APIView):
    """
    Handles user registration.
    """

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Handles user login.
    """

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleLoginView(APIView):

    def post(self, request):

        id_token = request.data.get("token")

        if not id_token:
            return Response(
                {"detail": "Token required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:

            decoded_token = firebase_auth.verify_id_token(id_token)

            email = decoded_token.get("email")
            name = decoded_token.get("name")
            picture = decoded_token.get("picture")

            user = User.objects.filter(email__iexact=email).first()

            if user is None:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=name or "",
                )

            else:

                if name and not user.first_name:
                    user.first_name = name
                    user.save()

            profile = user.profile

            if picture and profile.photo_url != picture:

                profile.photo_url = picture
                profile.save()

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )

        except Exception as e:

            return Response(
                {"detail": "Invalid Firebase token", "error": str(e)},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    def post(self, request):
        id_token = request.data.get("token")

        if not id_token:
            return Response(
                {"detail": "Token required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Verify Firebase token
            decoded_token = firebase_auth.verify_id_token(id_token)

            email = decoded_token.get("email")
            name = decoded_token.get("name")
            picture = decoded_token.get("picture")

            # Look up user by email (prevents duplicates)
            user = User.objects.filter(email__iexact=email).first()

            if user is None:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=name or "",
                    password=None,  # Google users won't use a password
                )
            else:
                updated = False

                if name and not user.first_name:
                    user.first_name = name
                    updated = True

                if updated:
                    user.save()

            # Create or get the user's profile
            profile = user.profile
            # Save the Google profile picture if we don't already have one
            if picture and profile.photo_url != picture:
                profile.photo_url = picture
                profile.save()

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "detail": "Invalid Firebase token",
                    "error": str(e),
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
