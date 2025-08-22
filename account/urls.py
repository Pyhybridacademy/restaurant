from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    # API endpoints
    path('api/register/', views.register, name='api_register'),
    path('api/login/', views.login_view, name='api_login'),
    path('api/logout/', views.logout_view, name='api_logout'),
    path('api/profile/', views.user_profile, name='api_profile'),
    
    # Template views
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
]
