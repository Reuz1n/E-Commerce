#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Product

def create_sample_products():
    """Crear productos de ejemplo para la tienda"""
    
    # Eliminar productos existentes
    Product.objects.all().delete()
    
    # Crear productos de ejemplo
    products_data = [
        {
            'name': 'Laptop Gaming Pro',
            'description': 'Laptop de alto rendimiento para gaming con procesador Intel i7, 16GB RAM y GPU RTX 3060',
            'price': 1299.99,
            'stock': 15
        },
        {
            'name': 'Smartphone Galaxy S23',
            'description': 'Smartphone Samsung con cámara de 108MP, 256GB de almacenamiento y batería de 5000mAh',
            'price': 899.99,
            'stock': 25
        },
        {
            'name': 'Auriculares Wireless Sony',
            'description': 'Auriculares inalámbricos con cancelación de ruido activa y 30 horas de batería',
            'price': 299.99,
            'stock': 30
        },
        {
            'name': 'Tablet iPad Air',
            'description': 'Tablet Apple con chip M1, pantalla de 10.9 pulgadas y compatibilidad con Apple Pencil',
            'price': 599.99,
            'stock': 12
        },
        {
            'name': 'Smartwatch Apple Watch',
            'description': 'Reloj inteligente con monitor cardíaco, GPS y resistencia al agua',
            'price': 399.99,
            'stock': 20
        },
        {
            'name': 'Cámara DSLR Canon',
            'description': 'Cámara réflex digital con sensor de 24.1MP y grabación de video 4K',
            'price': 799.99,
            'stock': 8
        },
        {
            'name': 'Consola PlayStation 5',
            'description': 'Consola de videojuegos de nueva generación con SSD ultrarrápido',
            'price': 499.99,
            'stock': 5
        },
        {
            'name': 'Monitor Gaming 27"',
            'description': 'Monitor curvo con resolución 1440p, 165Hz y tiempo de respuesta 1ms',
            'price': 349.99,
            'stock': 18
        }
    ]
    
    for product_data in products_data:
        Product.objects.create(**product_data)
    
    print(f"✅ Se crearon {len(products_data)} productos de ejemplo")
    print("Productos creados:")
    for product in Product.objects.all():
        print(f"  - {product.name}: ${product.price} (Stock: {product.stock})")

if __name__ == '__main__':
    create_sample_products() 