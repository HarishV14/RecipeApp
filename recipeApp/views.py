from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView, DetailView
from .models import Recipe, RecipeCollection
from django.core.paginator import Paginator


class HomePageView(TemplateView):
    template_name = 'home.html'
    

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/list.html'
    context_object_name = 'recipes'
    paginate_by = 3

    def get_queryset(self):
        return Recipe.objects.filter(featured=False).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        featured_recipes = Recipe.objects.filter(featured=True).order_by('-created_at')
        featured_paginator = Paginator(featured_recipes, 3)  
        featured_page_number = self.request.GET.get('featured_page')
        
        normal_recipes = Recipe.objects.filter(featured=False).order_by('-created_at')
        normal_paginator = Paginator(normal_recipes, self.paginate_by)
        page_number = self.request.GET.get('page')
        
        context['featured_recipes_page_obj'] = featured_paginator.get_page(featured_page_number)
        context['recipes_page_obj'] = normal_paginator.get_page(page_number)
        context['users'] = User.objects.all()
        context['cuisine_choices'] = Recipe.CuisineType.choices
        context['difficulty_choices'] = Recipe.DifficultyLevel.choices
        context['food_type_choices'] = Recipe.FoodType.choices

        return context


class RecipeCollectionListView(ListView):
    model = RecipeCollection
    template_name = 'collections/list.html'  
    context_object_name = 'collections'
    paginate_by = 3

    def get_queryset(self):
        return RecipeCollection.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection_count'] = RecipeCollection.objects.count()  
        return context


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'
    context_object_name = 'recipe'


class RecipeCollectionDetailView(DetailView):
    model = RecipeCollection
    template_name = 'collections/detail.html'
    context_object_name = 'collection'