# store/views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required   
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Order, Product
from .serializers import UserSerializer, CartSerializer, CartItemSerializer, OrderSerializer, ProductSerializer, serializers
from .forms import CustomUserCreationForm, ProductForm 
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


User = get_user_model()   

class MainView(View):
    def get(self, request):
        return render(request, 'store/main.html')

class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = cart.items.all()
        return render(request, 'store/cart.html', {'cart_items': items})

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

@method_decorator(csrf_protect, name='dispatch')
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
    


@login_required
def product_create_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store:product_list')  # o a donde prefieras
    else:
        form = ProductForm()
    return render(request, 'store/product_create.html', {'form': form})

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductListView(generics.ListAPIView):
    
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

def logout_view(request):
    logout(request)
    return redirect('store:login')

def main_view(request):
    return render(request, 'store/main.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('store:main')  # Redirige a la página de inicio o a otra página
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Iniciar sesión automáticamente después del registro
            return redirect('store:home')  # Redirige a la página de inicio o a otra página
    else:
        form = CustomUserCreationForm()
    return render(request, 'store/register.html', {'form': form})

@login_required
def cart_view(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)

    items = cart.items.all()
    return render(request, 'store/cart.html', {'cart_items': items})