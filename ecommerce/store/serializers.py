# store/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CartItem, Cart, Product, Order  # Asegúrate de que existan estos modelos

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Incluye detalles del producto
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'cart']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  # Incluye los items del carrito

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'total_amount', 'is_paid', 'created_at']
