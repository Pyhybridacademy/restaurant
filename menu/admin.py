from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Food


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'foods_count', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    
    def foods_count(self, obj):
        count = obj.foods.filter(is_available=True).count()
        return format_html(
            '<span style="font-weight: bold; color: #28a745;">{}</span>',
            count
        )
    foods_count.short_description = 'Available Foods'


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'price', 'is_available', 'availability_status', 
        'image_preview', 'created_at'
    ]
    list_filter = ['category', 'is_available', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_available', 'price']
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'price', 'is_available')
        }),
        ('Details', {
            'fields': ('description', 'image', 'image_preview')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def availability_status(self, obj):
        if obj.is_available:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">✓ Available</span>'
            )
        else:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">✗ Unavailable</span>'
            )
    availability_status.short_description = 'Status'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 150px; border-radius: 4px;"/>',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Image Preview'
    
    actions = ['make_available', 'make_unavailable']
    
    def make_available(self, request, queryset):
        updated = queryset.update(is_available=True)
        self.message_user(request, f'{updated} items marked as available.')
    make_available.short_description = "Mark selected items as available"
    
    def make_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(request, f'{updated} items marked as unavailable.')
    make_unavailable.short_description = "Mark selected items as unavailable"
