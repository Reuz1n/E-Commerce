from django.urls import path, include
from .views import CartView, CartItemCreateAPIView, CartItemDeleteView, CheckoutView, CartListView, ProductDetailView, ProductListView, register, login_view, main_view, product_create_view, logout_view
from .views import home
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

app_name = 'store'

urlpatterns = [
    path('', home, name='home'),
    path('main/', main_view, name='main'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/items/', CartItemCreateAPIView.as_view(), name='cart_item_create'),
    path('cart/items/<int:pk>/', CartItemDeleteView.as_view(), name='cart_item_delete'),
    path('cart/items/list/', CartListView.as_view(), name='cart-list'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('products/create/', product_create_view, name='product_create'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)