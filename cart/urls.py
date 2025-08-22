from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # API endpoints
    path('api/items/', views.cart_items, name='api_cart_items'),
    path('api/add/', views.add_to_cart, name='api_add_to_cart'),
    path('api/update/<int:item_id>/', views.update_cart_item, name='api_update_cart_item'),
    path('api/remove/<int:item_id>/', views.remove_from_cart, name='api_remove_from_cart'),
    
    # Template views
    path('', views.cart_page, name='cart'),
]
