from django.urls import path
from . import views


app_name = 'front'


urlpatterns = [
    path('', views.index, name='index'),
    path('category/<str:code>/', views.product_list, name='product_list'),
    path('product/<str:code>/', views.product_detail, name='product_detail'),
    path('product_delete/<int:id>/',views.product_delete, name='product_delete'),
    path('products/',views.all_products, name='all_products'),
    path('cart/', views.carts, name='cart'),
    path('cart/<str:code>/', views.cart_detail, name='cart_detail'),
    path('add-to-cart/<str:code>', views.add_to_cart, name='add_to_cart'),
    path('active/cart/', views.active_cart, name='active_cart'),
    path('order-list/', views.order_list, name='order_list'),


]