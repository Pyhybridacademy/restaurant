from rest_framework import serializers
from .models import Order, OrderItem
from cart.serializers import CartSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['food_name', 'food_price', 'quantity', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    order_number = serializers.CharField(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'status', 'total', 'customer_name', 
            'customer_phone', 'customer_email', 'delivery_address',
            'receipt', 'payment_method', 'payment_notes', 'items',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['total', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'customer_name', 'customer_phone', 'customer_email', 
            'delivery_address', 'receipt', 'payment_method', 'payment_notes'
        ]
