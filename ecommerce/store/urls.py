from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CartView, CartItemCreateAPIView, CartItemDeleteView, CheckoutView

urlpatterns = [
    # Rutas para autenticación con JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Rutas para carrito de compras
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/items/', CartItemCreateAPIView.as_view(), name='cart_item_create'),
    path('cart/items/<int:pk>/', CartItemDeleteView.as_view(), name='cart_item_delete'),
    
    # Ruta para el checkout
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
