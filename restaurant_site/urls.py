"""
URL configuration for restaurant_site project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('account/', include('account.urls')),
    path('menu/', include('menu.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('reservation/', include('reservation.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom admin site configuration
admin.site.site_header = "Restaurant Management System"
admin.site.site_title = "Restaurant Admin"
admin.site.index_title = "Welcome to Restaurant Management"
