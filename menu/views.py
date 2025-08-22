from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Food
from .serializers import CategorySerializer, FoodSerializer
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
import json


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class FoodListView(generics.ListAPIView):
    serializer_class = FoodSerializer
    
    def get_queryset(self):
        return Food.objects.filter(is_available=True)


@api_view(['GET'])
def foods_by_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        foods = Food.objects.filter(category=category, is_available=True)
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)


# Template views
def menu_page(request):
    return render(request, 'menu/menu.html')


@cache_page(60 * 5)  # Cache for 5 minutes
@require_http_methods(["GET"])
def categories_json(request):
    """Fast JSON endpoint for categories"""
    cache_key = 'categories_list'
    categories_data = cache.get(cache_key)
    
    if categories_data is None:
        categories = Category.objects.all().values('id', 'name', 'description')
        categories_data = list(categories)
        cache.set(cache_key, categories_data, 60 * 10)  # Cache for 10 minutes
    
    return JsonResponse({
        'categories': categories_data,
        'success': True
    })

@cache_page(60 * 2)  # Cache for 2 minutes
@require_http_methods(["GET"])
def foods_json(request):
    """Fast JSON endpoint for all available foods"""
    category_id = request.GET.get('category')
    cache_key = f'foods_list_{category_id or "all"}'
    foods_data = cache.get(cache_key)
    
    if foods_data is None:
        foods_query = Food.objects.filter(is_available=True).select_related('category')
        
        if category_id:
            foods_query = foods_query.filter(category_id=category_id)
        
        foods_data = list(foods_query.values(
            'id', 'name', 'description', 'price', 'image',
            'category__name', 'category__id'
        ))
        cache.set(cache_key, foods_data, 60 * 5)  # Cache for 5 minutes
    
    return JsonResponse({
        'foods': foods_data,
        'success': True
    })
