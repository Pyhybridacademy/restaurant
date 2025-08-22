from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from menu.models import Food
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from decimal import Decimal


def get_or_create_cart(request):
    """Get or create cart for user or session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


@api_view(['GET'])
def cart_items(request):
    cart = get_or_create_cart(request)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def add_to_cart(request):
    cart = get_or_create_cart(request)
    food_id = request.data.get('food_id')
    quantity = request.data.get('quantity', 1)
    
    try:
        food = Food.objects.get(id=food_id, is_available=True)
    except Food.DoesNotExist:
        return Response({'error': 'Food item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        food=food,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += int(quantity)
        cart_item.save()
    
    cache_key = f'cart_items_{cart.id}'
    cache.delete(cache_key)
    
    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['PUT'])
def update_cart_item(request, item_id):
    cart = get_or_create_cart(request)
    try:
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
        quantity = request.data.get('quantity', 1)
        
        if quantity <= 0:
            cart_item.delete()
            cache_key = f'cart_items_{cart.id}'
            cache.delete(cache_key)
            return Response({'message': 'Item removed from cart'})
        
        cart_item.quantity = quantity
        cart_item.save()
        
        cache_key = f'cart_items_{cart.id}'
        cache.delete(cache_key)
        
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['DELETE'])
def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request)
    try:
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
        cart_item.delete()
        
        cache_key = f'cart_items_{cart.id}'
        cache.delete(cache_key)
        
        return Response({'message': 'Item removed from cart'})
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)


# Template views
def cart_page(request):
    return render(request, 'cart/cart.html')


@require_http_methods(["GET"])
def cart_items_json(request):
    """Fast JSON endpoint for cart items"""
    cart = get_or_create_cart(request)
    cache_key = f'cart_items_{cart.id}'
    cart_data = cache.get(cache_key)
    
    if cart_data is None:
        cart_items = CartItem.objects.filter(cart=cart).select_related('food', 'food__category')
        
        items_data = []
        total_price = Decimal('0.00')
        total_items = 0
        
        for item in cart_items:
            item_total = item.food.price * item.quantity
            total_price += item_total
            total_items += item.quantity
            
            items_data.append({
                'id': item.id,
                'food_id': item.food.id,
                'food_name': item.food.name,
                'food_price': str(item.food.price),
                'food_image': item.food.image.url if item.food.image else None,
                'quantity': item.quantity,
                'total_price': str(item_total)
            })
        
        cart_data = {
            'items': items_data,
            'total_price': str(total_price),
            'total_items': total_items,
            'success': True
        }
        
        # Cache for 1 minute (short cache since cart changes frequently)
        cache.set(cache_key, cart_data, 60)
    
    return JsonResponse(cart_data)
