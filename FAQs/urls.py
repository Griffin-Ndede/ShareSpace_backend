from django.urls import path
from . import views

urlpatterns = [
    path('FAQs/', views.FAQs, name='FAQs'),
]