from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Order
from .utils import send_status_update_email
from datetime import datetime


@receiver(pre_save, sender=Order)
def track_status_change(sender, instance, **kwargs):
    """Track order status changes"""
    if instance.pk:
        try:
            old_instance = Order.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except Order.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Order)
def handle_status_change(sender, instance, created, **kwargs):
    """Handle order status changes"""
    if not created and hasattr(instance, '_old_status'):
        old_status = instance._old_status
        new_status = instance.status
        
        if old_status != new_status:
            # Send status update email
            send_status_update_email(instance, old_status, new_status)
            
            # Update timestamps based on status
            if new_status == 'confirmed' and not instance.confirmed_at:
                instance.confirmed_at = datetime.now()
                instance.save(update_fields=['confirmed_at'])
            elif new_status == 'delivered' and not instance.delivered_at:
                instance.delivered_at = datetime.now()
                instance.save(update_fields=['delivered_at'])
