from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import path
from django.shortcuts import render
from django.db.models import Count, Sum
from django.utils.html import format_html
from order.models import Order
from order.utils import get_order_statistics
from menu.models import Food, Category
from cart.models import Cart


class RestaurantAdminSite(AdminSite):
    site_header = "Restaurant Management System"
    site_title = "Restaurant Admin"
    index_title = "Welcome to Restaurant Management"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        """Custom dashboard view with statistics"""
        stats = get_order_statistics()
        
        # Get recent orders
        recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]
        
        # Get popular items
        popular_items = Food.objects.annotate(
            order_count=Count('cartitem__cart__order')
        ).order_by('-order_count')[:5]
        
        # Get pending orders that need attention
        pending_orders = Order.objects.filter(
            status__in=['pending', 'paid']
        ).order_by('created_at')
        
        context = {
            'title': 'Dashboard',
            'stats': stats,
            'recent_orders': recent_orders,
            'popular_items': popular_items,
            'pending_orders': pending_orders,
            'has_permission': True,
        }
        
        return render(request, 'admin/dashboard.html', context)


# Create custom admin site instance
admin_site = RestaurantAdminSite(name='restaurant_admin')
