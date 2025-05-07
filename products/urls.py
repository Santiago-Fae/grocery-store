from django.urls import path
from . import views

urlpatterns = [
    # Product routes
    path('', views.ProductListView.as_view(), name='product_list'),
    path('create/', views.ProductCreateView.as_view(), name='product_create'),
    path('edit/<int:pk>/', views.ProductUpdateView.as_view(), name='product_edit'),
    
    # Customer routes
    path('profile/', views.customer_profile, name='customer_profile'),
    
    # Basket routes
    path('basket/', views.basket_view, name='basket'),
    path('basket/add/<int:product_id>/', views.add_to_basket, name='add_to_basket'),
    path('basket/update/<int:item_id>/', views.update_basket_item, name='update_basket_item'),
    path('basket/remove/<int:item_id>/', views.remove_from_basket, name='remove_from_basket'),
    
    # Staff routes
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/basket/<int:basket_id>/', views.basket_detail_staff, name='basket_detail_staff'),
    path('staff/customers/', views.customer_search, name='customer_search'),
    path('staff/customers/<int:customer_id>/', views.customer_detail_staff, name='customer_detail_staff'),
] 