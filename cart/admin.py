from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['food', 'quantity', 'subtotal', 'created_at']
    can_delete = False


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_owner', 'total_items', 'total_price', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'session_key']
    readonly_fields = ['total_price', 'total_items', 'created_at', 'updated_at']
    inlines = [CartItemInline]
    
    def cart_owner(self, obj):
        if obj.user:
            return format_html(
                '<strong>{}</strong> ({})',
                obj.user.username,
                obj.user.email
            )
        else:
            return format_html(
                '<em>Guest</em> ({})',
                obj.session_key[:10] + '...' if obj.session_key else 'No session'
            )
    cart_owner.short_description = 'Owner'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').prefetch_related('items__food')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart_owner', 'food', 'quantity', 'subtotal', 'created_at']
    list_filter = ['created_at', 'food__category']
    search_fields = ['cart__user__username', 'food__name']
    readonly_fields = ['subtotal', 'created_at', 'updated_at']
    
    def cart_owner(self, obj):
        if obj.cart.user:
            return obj.cart.user.username
        return f"Guest ({obj.cart.session_key[:10]}...)"
    cart_owner.short_description = 'Cart Owner'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('cart__user', 'food')
