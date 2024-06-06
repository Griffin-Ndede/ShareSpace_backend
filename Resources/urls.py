from django.urls import path
from . import views

urlpatterns = [
    path('FAQs/', views.FAQsListView.as_view(), name='FAQs'), #get request
    path('FAQs/create/', views.FAQsCreateView.as_view(), name='message-create'), #post request
    path('categories/', views.CategoriesView.as_view(), name = 'Categories'),
]