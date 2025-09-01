from django.urls import path
from . import views
from .views import Home

urlpatterns = [
    path('', Home.as_view()),
    path('FAQs/', views.FAQsListView.as_view(), name='FAQs'), #get request
    path('FAQs/create/', views.FAQsCreateView.as_view(), name='message-create'), #post request
    path('categories/', views.CategoriesView.as_view(), name = 'Categories'),
    path('products/', views.ProductsView.as_view(), name="products"),
    path('products/<int:id>/', views.ProductDetailsView.as_view(), name="productdetails"),
    path('submit_contact_form/', views.SubmitContactFormView.as_view(), name='submit_contact_form')
]