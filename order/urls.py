from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    # API endpoints
    path('api/checkout/', views.checkout, name='api_checkout'),
    path('api/status/<int:order_id>/', views.order_status, name='api_order_status'),
    path('api/list/', views.user_orders, name='api_user_orders'),
    path('api/cancel/<int:order_id>/', views.cancel_order, name='api_cancel_order'),
    
    # Template views
    path('checkout/', views.checkout_page, name='checkout'),
    path('tracking/<int:order_id>/', views.order_tracking_page, name='tracking'),
    path('orders/', views.orders_page, name='orders'),
]
