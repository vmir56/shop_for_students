from django.urls import path
from . import views
app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('catalog/',views.create_product,name='catalog'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
]
