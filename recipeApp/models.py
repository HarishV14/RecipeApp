from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
            
    class FoodType(models.IntegerChoices):
        VEGETARIAN = 1, 'Veg'
        NON_VEGETARIAN = 2, 'Non-Veg'
        VEGAN = 3, 'Vegan'
    
        
    class CuisineType(models.IntegerChoices):
        SOUTH_INDIAN = 1, 'South Indian'
        NORTH_INDIAN = 2, 'North Indian'
        CHINESE = 3, 'Chinese'
        
        
    class DifficultyLevel(models.IntegerChoices):
        EASY = 1, 'Easy'
        MEDIUM = 2, 'Medium'
        HARD = 3, 'Hard'
    
    
    author = models.ForeignKey(User, related_name="recipes", on_delete=models.CASCADE)
    title = models.CharField(max_length = 255)
    servings = models.PositiveIntegerField()
    prepration_time = models.DurationField(help_text="Preparation time (hh:mm:ss)")
    total_time = models.DurationField(help_text="Total time (hh:mm:ss)")
    calories = models.PositiveIntegerField()
    instructions = models.TextField()
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cuisine = models.PositiveSmallIntegerField(choices=CuisineType.choices)
    food_type = models.PositiveSmallIntegerField(choices=FoodType.choices)
    difficulty = models.PositiveSmallIntegerField(choices=DifficultyLevel.choices)
    
    def get_total_ingredients(self):
        return self.ingredients.count()
    
    def is_featured_recipe(self):
        return self.featured
    
    def __str__(self):
        return self.title
    
    
class RecipeImage(models.Model):
    
    recipe = models.ForeignKey(Recipe, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='recipe_images/')
    uploaded_at = models.DateTimeField(auto_now_add = True)
    description = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"Image for {self.recipe.title}"
    
    
class RecipeIngredient(models.Model):
    
    class UnitType(models.IntegerChoices):
        GRAMS = 1, 'gms'
        NUMBERS = 2, 'number'
        TEASPOON = 3, 'tsp'
        TABLESPOON = 4, 'tbsp'
        LITERS = 5, 'litres'
        CUP = 6, 'cup'
    
    
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.PositiveSmallIntegerField(choices=UnitType.choices)
    optional = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} {self.get_unit_display()} of {self.name}"
    
    
class RecipeCollection(models.Model):
    
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='recipe_collections', on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe, related_name='collections')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def recipe_count(self):
        return self.recipes.count()

    def __str__(self):
        return f"{self.title} ({self.recipe_count()} recipes)"