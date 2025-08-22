from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['food_name', 'food_price', 'quantity', 'subtotal']
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'customer_name', 'customer_phone', 
        'status', 'colored_status', 'total', 'payment_method', 'created_at'
    ]
    list_filter = ['status', 'created_at', 'payment_method']
    search_fields = ['customer_name', 'customer_email', 'customer_phone', 'order_number']
    list_editable = ['status']
    readonly_fields = ['order_number', 'total', 'created_at', 'updated_at', 'user', 'cart']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'cart', 'status', 'total', 'created_at', 'updated_at')
        }),
        ('Customer Details', {
            'fields': ('customer_name', 'customer_phone', 'customer_email', 'delivery_address')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'receipt_preview', 'payment_notes')
        }),
        ('Timestamps', {
            'fields': ('confirmed_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
    )
    
    def colored_status(self, obj):
        colors = {
            'pending': '#ffc107',
            'paid': '#17a2b8',
            'confirmed': '#28a745',
            'preparing': '#fd7e14',
            'ready': '#6f42c1',
            'delivered': '#28a745',
            'cancelled': '#dc3545'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    colored_status.short_description = 'Status'
    
    def receipt_preview(self, obj):
        if obj.receipt:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-height: 100px; max-width: 200px;"/></a>',
                obj.receipt.url,
                obj.receipt.url
            )
        return "No receipt uploaded"
    receipt_preview.short_description = 'Receipt'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    actions = ['mark_as_confirmed', 'mark_as_preparing', 'mark_as_ready', 'mark_as_delivered']
    
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} orders marked as confirmed.')
    mark_as_confirmed.short_description = "Mark selected orders as confirmed"
    
    def mark_as_preparing(self, request, queryset):
        updated = queryset.update(status='preparing')
        self.message_user(request, f'{updated} orders marked as preparing.')
    mark_as_preparing.short_description = "Mark selected orders as preparing"
    
    def mark_as_ready(self, request, queryset):
        updated = queryset.update(status='ready')
        self.message_user(request, f'{updated} orders marked as ready.')
    mark_as_ready.short_description = "Mark selected orders as ready"
    
    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} orders marked as delivered.')
    mark_as_delivered.short_description = "Mark selected orders as delivered"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'food_name', 'quantity', 'food_price', 'subtotal']
    list_filter = ['order__status', 'order__created_at']
    search_fields = ['food_name', 'order__customer_name']
    readonly_fields = ['order', 'food_name', 'food_price', 'quantity', 'subtotal']
