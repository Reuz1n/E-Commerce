
from django.urls import path
from .views import CartView, CartItemCreateAPIView, CartItemDeleteView, CheckoutView, TokenObtainPairView, TokenRefreshView, ProductCreateView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/items/', CartItemCreateAPIView.as_view(), name='cart_item_create'),
    path('cart/items/<int:pk>/', CartItemDeleteView.as_view(), name='cart_item_delete'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('products/', ProductCreateView.as_view(), name='product_create'),
]