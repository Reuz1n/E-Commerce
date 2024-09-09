# store/views.py

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Cart, CartItem, Order
from .serializers import UserSerializer, CartSerializer, CartItemSerializer, OrderSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError({'username': 'A user with that username already exists.'})
        return super().post(request, *args, **kwargs)

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
        # Asociar el item con el carrito del usuario autenticado
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)

class CartItemDeleteView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtrar los artículos del carrito por el usuario autenticado
        cart = Cart.objects.get(user=self.request.user)
        return self.queryset.filter(cart=cart)

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Obtener el carrito del usuario
        cart = Cart.objects.get(user=request.user)
        items = cart.items.all()
        
        if not items:
            return Response({"error": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Calcular el total
        total_amount = sum(item.product.price * item.quantity for item in items)

        # Crear una orden
        order = Order.objects.create(user=request.user, total_amount=total_amount)

        # Simular respuesta de pago exitosa
        mock_response = {
            'client_secret': 'mock_client_secret_12345',  # Valor estático simulado
            'status': 'success'
        }

        # Marcar la orden como pagada (simulado)
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