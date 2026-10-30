from datetime import timedelta
from django.contrib.auth import authenticate, get_user_model
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
    UserSerializer,
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
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginView(APIView):
    """
    Handles user login and returns JWT tokens
    together with authenticated user details.
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

            if user is not None:
                if not user.is_active:
                    return Response(
                        {"detail": "This account has been deactivated."},
                        status=status.HTTP_403_FORBIDDEN,
                    )

                refresh = RefreshToken.for_user(user)

                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "user": UserSerializer(user).data,
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
            email_verified = decoded_token.get("email_verified", False)

            if not email:
                return Response(
                    {"detail": "Firebase token did not contain an email"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Find an existing account by email.
            user = User.objects.filter(email__iexact=email).first()

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

            # Reject inactive accounts.
            if not user.is_active:
                return Response(
                    {"detail": "This account has been deactivated."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Update the profile picture if available.
            profile = user.profile

            if picture and profile.photo_url != picture:
                profile.photo_url = picture
                profile.save(update_fields=["photo_url"])

            # Issue JWT tokens.
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as error:
            print("Google login error:", str(error))

            return Response(
                {"detail": "Invalid Firebase token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class UserStatisticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        now = timezone.now()
        today = timezone.localdate()

        # Date boundaries
        start_of_today = timezone.make_aware(
            timezone.datetime.combine(
                today,
                timezone.datetime.min.time(),
            )
        )

        start_of_week = start_of_today - timedelta(days=today.weekday())
        start_of_month = start_of_today.replace(day=1)

        # User counts
        total_users = User.objects.count()

        users_today = User.objects.filter(date_joined__gte=start_of_today).count()

        users_this_week = User.objects.filter(date_joined__gte=start_of_week).count()

        users_this_month = User.objects.filter(date_joined__gte=start_of_month).count()

        # Daily signups for the past seven days
        daily_signups = []

        for days_ago in range(6, -1, -1):
            day = today - timedelta(days=days_ago)

            day_start = timezone.make_aware(
                timezone.datetime.combine(
                    day,
                    timezone.datetime.min.time(),
                )
            )

            day_end = day_start + timedelta(days=1)

            count = User.objects.filter(
                date_joined__gte=day_start,
                date_joined__lt=day_end,
            ).count()

            daily_signups.append(
                {
                    "date": day.isoformat(),
                    "count": count,
                }
            )

        # Latest ten users
        recent_users = User.objects.order_by("-date_joined")[:10]

        recent_users_data = []

        for user in recent_users:
            # Retrieve associated profile safely.
            try:
                profile = user.profile
            except Exception:
                profile = None

            phone = ""
            location = ""

            if profile:
                phone = (
                    getattr(profile, "phone_number", "")
                    or getattr(profile, "phone", "")
                    or ""
                )

                location = getattr(profile, "location", "") or ""

            role = getattr(user, "role", None)

            recent_users_data.append(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    # Marketplace classification
                    "role": role,
                    "roles": [role] if role else [],
                    # Administrator permissions
                    "is_staff": user.is_staff,
                    "is_superuser": user.is_superuser,
                    # Account status
                    "is_active": user.is_active,
                    "status": "Active" if user.is_active else "Suspended",
                    # Verification
                    "verification_status": getattr(
                        user,
                        "verification_status",
                        "unverified",
                    ),
                    "verification": getattr(
                        user,
                        "verification_status",
                        "unverified",
                    )
                    .replace("_", " ")
                    .title(),
                    # Profile information
                    "phone": phone,
                    "location": location or "Location not provided",
                    # Listing and booking counts
                    "listingsCount": None,
                    "bookingsCount": None,
                    # Dates
                    "date_joined": user.date_joined,
                    "joinedAt": user.date_joined,
                    "last_login": user.last_login,
                    "lastActiveAt": user.last_login,
                    # Display name
                    "name": (user.get_full_name() or user.username),
                }
            )

        return Response(
            {
                "total_users": total_users,
                "users_today": users_today,
                "users_this_week": users_this_week,
                "users_this_month": users_this_month,
                "daily_signups": daily_signups,
                "recent_users": recent_users_data,
            }
        )
