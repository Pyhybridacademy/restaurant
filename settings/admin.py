from django.contrib import admin
from .models import SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'site_tagline', 'logo', 'favicon')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'whatsapp_number'),
            'classes': ('collapse',)
        }),
        ('SEO Settings', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Business Hours', {
            'fields': (
                'monday_hours', 'tuesday_hours', 'wednesday_hours', 'thursday_hours',
                'friday_hours', 'saturday_hours', 'sunday_hours'
            ),
            'classes': ('collapse',)
        }),
        ('Business Settings', {
            'fields': ('delivery_fee', 'minimum_order', 'is_delivery_enabled', 'is_pickup_enabled'),
            'classes': ('collapse',)
        }),
        ('Footer', {
            'fields': ('footer_text',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def has_add_permission(self, request):
        # Only allow one settings instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of settings
        return False
