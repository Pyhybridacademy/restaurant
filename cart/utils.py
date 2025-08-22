from .models import Cart, CartItem
from django.contrib.auth.models import User


def merge_guest_cart_to_user(request, user):
    """
    Merge guest cart items to user cart when user logs in
    """
    if not request.session.session_key:
        return
    
    try:
        # Get guest cart
        guest_cart = Cart.objects.get(session_key=request.session.session_key)
        
        # Get or create user cart
        user_cart, created = Cart.objects.get_or_create(user=user)
        
        # Merge cart items
        for guest_item in guest_cart.items.all():
            user_item, created = CartItem.objects.get_or_create(
                cart=user_cart,
                food=guest_item.food,
                defaults={'quantity': guest_item.quantity}
            )
            
            if not created:
                # If item already exists, add quantities
                user_item.quantity += guest_item.quantity
                user_item.save()
        
        # Delete guest cart
        guest_cart.delete()
        
    except Cart.DoesNotExist:
        pass


def get_cart_count(request):
    """
    Get total number of items in cart
    """
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            return cart.total_items
        except Cart.DoesNotExist:
            return 0
    else:
        session_key = request.session.session_key
        if session_key:
            try:
                cart = Cart.objects.get(session_key=session_key)
                return cart.total_items
            except Cart.DoesNotExist:
                return 0
    return 0
