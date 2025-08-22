from django.db import models
from django.core.cache import cache

class SiteSettings(models.Model):
    # Basic Site Information
    site_name = models.CharField(max_length=100, default='Restaurant Site')
    site_tagline = models.CharField(max_length=200, default='Delicious food delivered fresh to your door')
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    
    # Contact Information
    phone = models.CharField(max_length=20, default='(555) 123-4567')
    email = models.EmailField(default='info@restaurant.com')
    address = models.TextField(default='123 Food Street, City')
    
    # Social Media
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True, help_text='Include country code (e.g., +1234567890)')
    
    # SEO Settings
    meta_description = models.TextField(max_length=160, default='Experience exceptional dining with fresh, delicious food delivered to your door.')
    meta_keywords = models.CharField(max_length=255, default='restaurant, food delivery, dining, fresh food')
    
    # Business Hours
    monday_hours = models.CharField(max_length=50, default='11:00 AM - 10:00 PM')
    tuesday_hours = models.CharField(max_length=50, default='11:00 AM - 10:00 PM')
    wednesday_hours = models.CharField(max_length=50, default='11:00 AM - 10:00 PM')
    thursday_hours = models.CharField(max_length=50, default='11:00 AM - 10:00 PM')
    friday_hours = models.CharField(max_length=50, default='11:00 AM - 11:00 PM')
    saturday_hours = models.CharField(max_length=50, default='11:00 AM - 11:00 PM')
    sunday_hours = models.CharField(max_length=50, default='12:00 PM - 9:00 PM')
    
    # Additional Settings
    delivery_fee = models.DecimalField(max_digits=5, decimal_places=2, default=2.99)
    minimum_order = models.DecimalField(max_digits=6, decimal_places=2, default=15.00)
    is_delivery_enabled = models.BooleanField(default=True)
    is_pickup_enabled = models.BooleanField(default=True)
    
    # Footer Content
    footer_text = models.TextField(default='© 2024 Restaurant Site. All rights reserved.')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
    
    def __str__(self):
        return f"Site Settings - {self.site_name}"
    
    def save(self, *args, **kwargs):
        # Clear cache when settings are updated
        cache.delete('site_settings')
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get site settings with caching"""
        settings = cache.get('site_settings')
        if settings is None:
            settings, created = cls.objects.get_or_create(pk=1)
            cache.set('site_settings', settings, 3600)  # Cache for 1 hour
        return settings
    
    @property
    def business_hours_dict(self):
        return {
            'Monday': self.monday_hours,
            'Tuesday': self.tuesday_hours,
            'Wednesday': self.wednesday_hours,
            'Thursday': self.thursday_hours,
            'Friday': self.friday_hours,
            'Saturday': self.saturday_hours,
            'Sunday': self.sunday_hours,
        }
