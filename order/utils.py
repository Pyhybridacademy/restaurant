from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Order


def send_order_confirmation_email(order):
    """Send order confirmation email to customer"""
    try:
        subject = f'Order Confirmation - #{order.order_number}'
        
        # Create email content
        context = {
            'order': order,
            'items': order.items.all(),
        }
        
        message = f"""
        Dear {order.customer_name},
        
        Thank you for your order! Here are the details:
        
        Order Number: #{order.order_number}
        Total: ${order.total}
        Status: {order.get_status_display()}
        
        Items:
        """
        
        for item in order.items.all():
            message += f"- {item.quantity}x {item.food_name} - ${item.subtotal}\n"
        
        message += f"""
        
        Customer Details:
        Name: {order.customer_name}
        Phone: {order.customer_phone}
        Email: {order.customer_email}
        """
        
        if order.delivery_address:
            message += f"Delivery Address: {order.delivery_address}\n"
        
        message += """
        
        You can track your order status at any time by visiting our website.
        
        Thank you for choosing our restaurant!
        
        Best regards,
        Restaurant Team
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.customer_email],
            fail_silently=True,
        )
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_status_update_email(order, old_status, new_status):
    """Send email when order status changes"""
    try:
        status_messages = {
            'paid': 'Your payment has been received and confirmed.',
            'confirmed': 'Your order has been confirmed and is being prepared.',
            'preparing': 'Your order is currently being prepared by our kitchen.',
            'ready': 'Your order is ready for pickup/delivery!',
            'delivered': 'Your order has been delivered. Enjoy your meal!',
            'cancelled': 'Your order has been cancelled. Please contact us if you have any questions.'
        }
        
        subject = f'Order Update - #{order.order_number}'
        message = f"""
        Dear {order.customer_name},
        
        Your order #{order.order_number} status has been updated.
        
        New Status: {order.get_status_display()}
        {status_messages.get(new_status, '')}
        
        You can track your order at any time by visiting our website.
        
        Thank you!
        Restaurant Team
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.customer_email],
            fail_silently=True,
        )
        
        return True
    except Exception as e:
        print(f"Error sending status update email: {e}")
        return False


def calculate_estimated_delivery_time(order):
    """Calculate estimated delivery time based on order status"""
    from datetime import datetime, timedelta
    
    base_time = order.created_at
    
    if order.status == 'pending':
        return base_time + timedelta(minutes=45)
    elif order.status == 'paid':
        return base_time + timedelta(minutes=40)
    elif order.status == 'confirmed':
        return base_time + timedelta(minutes=35)
    elif order.status == 'preparing':
        return base_time + timedelta(minutes=20)
    elif order.status == 'ready':
        return base_time + timedelta(minutes=10)
    else:
        return None


def get_order_statistics():
    """Get order statistics for admin dashboard"""
    from django.db.models import Count, Sum
    from datetime import datetime, timedelta
    
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    stats = {
        'total_orders': Order.objects.count(),
        'today_orders': Order.objects.filter(created_at__date=today).count(),
        'week_orders': Order.objects.filter(created_at__date__gte=week_ago).count(),
        'month_orders': Order.objects.filter(created_at__date__gte=month_ago).count(),
        'pending_orders': Order.objects.filter(status='pending').count(),
        'preparing_orders': Order.objects.filter(status='preparing').count(),
        'total_revenue': Order.objects.filter(status__in=['delivered', 'ready']).aggregate(
            total=Sum('total')
        )['total'] or 0,
        'status_breakdown': Order.objects.values('status').annotate(
            count=Count('id')
        ).order_by('status')
    }
    
    return stats
