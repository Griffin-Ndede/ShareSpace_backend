"""
URL configuration for ShareSpace_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("",include("Resources.urls")),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    

    path('admin/', admin.site.urls),

]  
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# available endpoints attached to the "api/v1/auth/" path

# /api/v1/auth/login/ dj_rest_auth.views.LoginView rest_login
# /api/v1/auth/logout/ dj_rest_auth.views.LogoutView rest_logout
# /api/v1/auth/password/change/ dj_rest_auth.views.PasswordChangeView rest_password_change
# /api/v1/auth/password/reset/ dj_rest_auth.views.PasswordResetView rest_password_reset
# /api/v1/auth/password/reset/confirm/ dj_rest_auth.views.PasswordResetConfirmView rest_password_reset_confirm
# /api/v1/auth/token/refresh/ dj_rest_auth.jwt_auth.RefreshViewWithCookieSupport token_refresh
# /api/v1/auth/token/verify/ rest_framework_simplejwt.views.TokenVerifyView token_verify
# /api/v1/auth/user/ dj_rest_auth.views.UserDetailsView rest_user_details