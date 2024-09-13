
from django.urls import path
from .views import CartView, CartItemCreateAPIView, CartItemDeleteView, CheckoutView, TokenObtainPairView, TokenRefreshView, ProductCreateView, CartListView, ProductDetailView, ProductListView, register, login_view

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/items/', CartItemCreateAPIView.as_view(), name='cart_item_create'),
    path('cart/items/<int:pk>/', CartItemDeleteView.as_view(), name='cart_item_delete'),
    path('cart/items/list/', CartListView.as_view(), name='cart-list'),  # Ruta para listar artículos del carrito
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/', ProductListView.as_view(), name='product_list'),  # Ruta para listar todos los productos
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('cart/items/', CartListView.as_view(), name='cart-list'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
]