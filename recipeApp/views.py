from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from .models import Recipe, RecipeCollection
from django.core.paginator import Paginator
from .forms import RecipeForm, RecipeImageFormSet, RecipeIngredientFormSet, RecipeCollectionForm
import json


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
 
 
class RecipeCollectionCreateView(FormView):
    form_class = RecipeCollectionForm
    template_name = 'collections/collection_form.html'  

    def form_valid(self, form):
        collection = form.save(commit=False)
        collection.user = self.request.user 
        collection.save() 
        form.save_m2m()  
        
        return redirect('collection_detail', pk=collection.pk)

    def form_invalid(self, form):
        return super().form_invalid(form)
    

class RecipeCollectionUpdate(UpdateView):
    model = RecipeCollection  
    form_class = RecipeCollectionForm
    template_name = 'collections/collection_form.html'  

    def get_object(self, queryset=None):
        return super().get_object(queryset)

    def form_valid(self, form):
        collection = form.save(commit=False)
        collection.user = self.request.user  
        collection.save() 
        form.save_m2m()  
        return redirect('collection_detail', pk=collection.pk)  

    def form_invalid(self, form):
        return super().form_invalid(form)


class RecipeCreateView(FormView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredient_formset'] = RecipeIngredientFormSet(prefix='ingredients')
        context['image_formset'] = RecipeImageFormSet(prefix='images')
        return context

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.author = self.request.user
        recipe.save()

        ingredient_formset = RecipeIngredientFormSet(self.request.POST, prefix='ingredients')

        if ingredient_formset.is_valid():
            ingredients = ingredient_formset.save(commit=False)
            for ingredient in ingredients:
                ingredient.recipe = recipe 
                ingredient.save()
        else:
            print(ingredient_formset.errors)  

        image_formset = RecipeImageFormSet(self.request.POST, self.request.FILES, prefix='images')
        
        if image_formset.is_valid():
            images = image_formset.save(commit=False)
            for image in images:
                image.recipe = recipe  
                image.save()
        else:
            print(image_formset.errors)  

        return redirect('recipe_detail', pk=recipe.pk)
    
    def form_invalid(self, form):
        ingredient_formset = RecipeIngredientFormSet(self.request.POST, prefix='ingredients')
        image_formset = RecipeImageFormSet(self.request.POST, self.request.FILES, prefix='images')
        return self.render_to_response({
            'form': form,
            'ingredient_formset': ingredient_formset,
            'image_formset': image_formset,
        })
            
            
class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.object
        context['ingredient_formset'] = RecipeIngredientFormSet(
            instance=recipe, prefix='ingredients'
        )
        context['image_formset'] = RecipeImageFormSet(
            instance=recipe, prefix='images'
        )
        context['initial_ingredients'] = json.dumps([
            {
                'id': ingredient.id,
                'name': ingredient.name,
                'quantity': ingredient.quantity,
                'unit': ingredient.unit,
                'optional': ingredient.optional,
            } for ingredient in recipe.ingredients.all()
        ])
        context['initial_images'] = json.dumps([
            {
                'id': image.id,
                'description': image.description,
                'url': image.image.url, 
            } for image in recipe.images.all()
        ])
        context['recipe'] = recipe
        return context

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.author = self.request.user  
        recipe.save()

        ingredient_formset = RecipeIngredientFormSet(self.request.POST, instance=recipe, prefix='ingredients')
        if ingredient_formset.is_valid():
            ingredient_formset.save() 
        else:
            print(ingredient_formset.errors)

        image_formset = RecipeImageFormSet(self.request.POST, self.request.FILES, instance=recipe, prefix='images')
        if image_formset.is_valid():
            image_formset.save()  
        else:
            print(image_formset.errors,"image")
            
        return redirect('recipe_detail', pk=recipe.pk)

    def form_invalid(self, form):
        ingredient_formset = RecipeIngredientFormSet(self.request.POST, instance=self.object, prefix='ingredients')
        image_formset = RecipeImageFormSet(self.request.POST, self.request.FILES, instance=self.object, prefix='images')
        initial_ingredients = json.dumps([
            {
                'id': ingredient.id,
                'name': ingredient.name,
                'quantity': ingredient.quantity,
                'unit': ingredient.unit,
                'optional': ingredient.optional,
            } for ingredient in form.instance.ingredients.all()
        ])
        initial_images = json.dumps([
            {
                'id': image.id,
                'description': image.description,
                'url': image.image.url, 
            } for image in form.instance.images.all()
        ])
        recipe = self.object
        return self.render_to_response({
            'form': form,
            'ingredient_formset': ingredient_formset,
            'image_formset': image_formset,
            'initial_ingredients':initial_ingredients,
            'initial_images':initial_images,
            'recipe':recipe
        })
