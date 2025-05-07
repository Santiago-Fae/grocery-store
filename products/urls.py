from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('create/', views.ProductCreateView.as_view(), name='product_create'),
    path('edit/<int:pk>/', views.ProductUpdateView.as_view(), name='product_edit'),
] 