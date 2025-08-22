from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer
from .utils import send_order_confirmation_email, calculate_estimated_delivery_time
from cart.models import Cart
from cart.views import get_or_create_cart


@api_view(['POST'])
def checkout(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = OrderCreateSerializer(data=request.data)
    if serializer.is_valid():
        # Create order
        order = serializer.save(
            user=request.user,
            cart=cart,
            total=cart.total_price
        )
        
        # Create order items (snapshot of cart items)
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                food_name=cart_item.food.name,
                food_price=cart_item.food.price,
                quantity=cart_item.quantity,
                subtotal=cart_item.subtotal
            )
        
        # Send confirmation email
        send_order_confirmation_email(order)
        
        # Clear cart after order creation
        cart.items.all().delete()
        
        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def order_status(request, order_id):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        serializer = OrderSerializer(order)
        
        # Add estimated delivery time
        data = serializer.data
        estimated_time = calculate_estimated_delivery_time(order)
        if estimated_time:
            data['estimated_delivery'] = estimated_time.isoformat()
        
        return Response(data)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def user_orders(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def cancel_order(request, order_id):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        
        # Only allow cancellation for pending or paid orders
        if order.status not in ['pending', 'paid']:
            return Response({
                'error': 'Order cannot be cancelled at this stage'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'cancelled'
        order.save()
        
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


# Template views
def checkout_page(request):
    return render(request, 'order/checkout.html')


def order_tracking_page(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order/tracking.html', {'order': order})


def orders_page(request):
    return render(request, 'order/orders.html')
