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
from django.views.generic.base import TemplateView  # new
from django.contrib import admin
from django.urls import include, path, re_path
from Apps.Accounts.views import GoogleLogin, GoogleLoginCallback, LoginPage


urlpatterns = [
    path("", include("Apps.Resources.urls")),
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),
    path("accounts/", include("Apps.Accounts.urls")),  # new
    path("accounts/", include("django.contrib.auth.urls")),  # new
    path("", TemplateView.as_view(template_name="home.html"), name="home"),  # new
    path("login/", LoginPage.as_view(), name="login"),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    re_path(r"^api/v1/auth/accounts/", include("allauth.urls")),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/v1/auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("api/v1/auth/google/callback/",GoogleLoginCallback.as_view(),name="google_login_callback",),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
