from django import forms
import django_filters
from .models import Recipe,RecipeCollection
from django.db.models import Q


class RecipeFilter(django_filters.FilterSet):
    
    search = django_filters.CharFilter(method='recipe_search_filter', label='Search')
    
    cuisine = django_filters.ChoiceFilter(choices=Recipe.CuisineType.choices, label='Cuisine', empty_label='All Cuisine types')
    difficulty = django_filters.ChoiceFilter(choices=Recipe.DifficultyLevel.choices, label='Difficulty')
    food_type = django_filters.ChoiceFilter(choices=Recipe.FoodType.choices, label='Food Type')
    
    sort_by_created = django_filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),      
            ('-created_at', 'created_at_desc'), 
        ),
        label='Sort by Created At'
    )

    sort_by_calories = django_filters.OrderingFilter(
        fields=(
            ('calories', 'calories'),            
            ('-calories', 'calories_desc'),      
        ),
        label='Sort by Calories'
    )
    
    user_filter = django_filters.BooleanFilter(method='filter_by_user', label='Show My Items')
    
    class Meta:
        model = Recipe
        fields = []
        
    def __init__(self, data=None, user=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self.user = user 
        
    def filter_by_user(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.user)
        return queryset
        
    def recipe_search_filter(self, queryset, name, value):
        cuisine_map = {str(v): k for k, v in dict(Recipe.CuisineType.choices).items()}
        if value:
            return queryset.filter(
                Q(title__icontains=value) | 
                Q(author__username__icontains=value) | 
                Q(cuisine__in=[k for v, k in cuisine_map.items() if value.lower() in v.lower()]) |
                Q(ingredients__name__icontains=value)
            ).distinct()
        return queryset


class RecipeCollectionFilter(django_filters.FilterSet):
    
    search = django_filters.CharFilter(method='collection_search_filter', label='Search')
    user_filter = django_filters.BooleanFilter(method='filter_by_user', label='Show My Items')
    
    class Meta:
        model = RecipeCollection
        fields = []
    
    def __init__(self, data=None, user=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self.user = user 
        
    def filter_by_user(self, queryset, name, value):
        if value:
            return queryset.filter(user__username=self.user)
        return queryset
    
    def collection_search_filter(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(title__icontains=value) | 
                Q(recipes__title__icontains=value) |
                Q(user__username__icontains=value)
            ).distinct()
        return queryset
    