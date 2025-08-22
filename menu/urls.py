from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    # API endpoints
    path('api/categories/', views.CategoryListView.as_view(), name='api_categories'),
    path('api/foods/', views.FoodListView.as_view(), name='api_foods'),
    path('api/foods/category/<int:category_id>/', views.foods_by_category, name='api_foods_by_category'),
    
    path('api/categories/json/', views.categories_json, name='categories_json'),
    path('api/foods/json/', views.foods_json, name='foods_json'),
    
    # Template views
    path('', views.menu_page, name='menu'),
]
