from django import forms
import django_filters
from .models import Recipe,RecipeCollection
from django.db.models import Q


class RecipeFilter(django_filters.FilterSet):
    
    search = django_filters.CharFilter(method='recipe_search_filter', label='Search')
    
    class Meta:
        model = Recipe
        fields = []
        
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
    
    class Meta:
        model = RecipeCollection
        fields = ['search',]
    
    def collection_search_filter(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(title__icontains=value) | 
                Q(recipes__title__icontains=value) |
                Q(user__username__icontains=value)
            ).distinct()
        return queryset
    