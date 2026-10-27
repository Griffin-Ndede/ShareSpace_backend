from django.urls import path
from .views import GoogleLoginView, RegisterView, LoginView, UserStatisticsView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("google-login/", GoogleLoginView.as_view(), name="google-login"),
    path("statistics/users/", UserStatisticsView.as_view(), name="user-statistics"),
]
