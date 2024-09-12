# store/views.py

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .models import Cart, CartItem, Order, Product
from .serializers import UserSerializer, CartSerializer, CartItemSerializer, OrderSerializer, ProductSerializer, serializers
from .forms import CustomUserCreationForm

User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Iniciar sesión automáticamente después del registro
            return redirect('home')  # Redirige a la página de inicio o a otra página
    else:
        form = CustomUserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirige a la página de inicio o a otra página
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Devuelve el carrito del usuario autenticado
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

class CartItemCreateAPIView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        # Obtén o crea el carrito para el usuario autenticado
        cart, created = Cart.objects.get_or_create(user=user)
        # Guarda el CartItem con el carrito asociado
        serializer.save(cart=cart)
        
class CartItemDeleteView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtrar los artículos del carrito por el usuario autenticado
        cart = Cart.objects.get(user=self.request.user)
        return self.queryset.filter(cart=cart)

class CartListView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return CartItem.objects.none()  # Retorna un queryset vacío si no hay carrito

        return CartItem.objects.filter(cart=cart)

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Obtener el carrito del usuario autenticado
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart does not exist for this user."}, status=status.HTTP_400_BAD_REQUEST)

        items = cart.items.all()
        
        if not items:
            return Response({"error": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        total_amount = sum(item.product.price * item.quantity for item in items)

        # Crear una orden con el usuario autenticado
        order = Order.objects.create(user=request.user, total_amount=total_amount)

        # Simular respuesta de pago exitosa
        mock_response = {
            'client_secret': 'mock_client_secret_12345',
            'status': 'success'
        }

        order.is_paid = True
        order.save()

        # Vaciar el carrito después del checkout
        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    
class TokenObtainPairView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class TokenRefreshView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')
        try:
            refresh = RefreshToken(refresh_token)
            new_access = str(refresh.access_token)
            return Response({'access': new_access})
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ExampleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({"message": "Acceso autorizado"})

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer