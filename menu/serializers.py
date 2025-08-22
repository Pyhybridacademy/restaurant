from rest_framework import serializers
from .models import Category, Food


class CategorySerializer(serializers.ModelSerializer):
    foods_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'foods_count']
    
    def get_foods_count(self, obj):
        return obj.foods.filter(is_available=True).count()


class FoodSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Food
        fields = ['id', 'name', 'price', 'description', 'image', 'category', 'category_name', 'is_available']
