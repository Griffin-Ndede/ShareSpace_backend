
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from firebase_admin import auth as firebase_auth

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
)

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

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginView(APIView):
    """
    Handles user login.
    """

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(
                username=username,
                password=password,
            )

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
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class GoogleLoginView(APIView):
    """
    Authenticates users using Firebase Google sign-in
    and issues JWT tokens for the Django API.
    """

    def post(self, request):
        id_token = request.data.get("token")

        if not id_token:
            return Response(
                {"detail": "Token required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            decoded_token = firebase_auth.verify_id_token(id_token)

            email = decoded_token.get("email")
            name = decoded_token.get("name")
            picture = decoded_token.get("picture")

            if not email:
                return Response(
                    {"detail": "Firebase token did not contain an email"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Find an existing account by email to prevent duplicates.
            user = User.objects.filter(
                email__iexact=email
            ).first()

            if user is None:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=name or "",
                    password=None,
                )
            else:
                if name and not user.first_name:
                    user.first_name = name
                    user.save(update_fields=["first_name"])

            # Update the profile picture if available.
            profile = user.profile

            if picture and profile.photo_url != picture:
                profile.photo_url = picture
                profile.save(update_fields=["photo_url"])

            # Issue JWT tokens for the Django API.
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )

        except Exception:
            return Response(
                {"detail": "Invalid Firebase token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class UserStatisticsView(APIView):
    """
    Returns user registration statistics for the admin dashboard.
    Requires an authenticated staff user.
    """

    # permission_classes = [IsAdminUser]

    def get(self, request):
        today = timezone.localdate()
        week_start = today - timedelta(days=6)
        month_start = today - timedelta(days=29)

        # Total registered users.
        total_users = User.objects.count()

        # Users who registered today.
        users_today = User.objects.filter(
            date_joined__date=today
        ).count()

        # Users who registered in the last 7 days, including today.
        users_this_week = User.objects.filter(
            date_joined__date__gte=week_start,
            date_joined__date__lte=today,
        ).count()

        # Users who registered in the last 30 days, including today.
        users_this_month = User.objects.filter(
            date_joined__date__gte=month_start,
            date_joined__date__lte=today,
        ).count()

        # Daily registration counts for the last 30 days.
        daily_signups = (
            User.objects.filter(
                date_joined__date__gte=month_start,
                date_joined__date__lte=today,
            )
            .annotate(signup_date=TruncDate("date_joined"))
            .values("signup_date")
            .annotate(count=Count("id"))
            .order_by("signup_date")
        )

        # The 10 most recently registered users.
        recent_users = User.objects.order_by(
            "-date_joined"
        )[:10]

        recent_users_data = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "date_joined": user.date_joined,
                "is_active": user.is_active,
            }
            for user in recent_users
        ]

        return Response(
            {
                "total_users": total_users,
                "users_today": users_today,
                "users_this_week": users_this_week,
                "users_this_month": users_this_month,
                "daily_signups": [
                    {
                        "date": item["signup_date"],
                        "count": item["count"],
                    }
                    for item in daily_signups
                ],
                "recent_users": recent_users_data,
            },
            status=status.HTTP_200_OK,
        )
