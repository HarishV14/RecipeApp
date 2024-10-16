from django.contrib import admin
from .models import Recipe, RecipeIngredient, RecipeCollection, RecipeImage

class RecipeImageInline(admin.TabularInline):
    model = RecipeImage
    extra = 1 
    
    
class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 2
    
    
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'cuisine', 'food_type', 'difficulty', 'calories', 'created_at', 'featured')
    list_filter = ('cuisine', 'food_type', 'difficulty', 'featured')
    search_fields = ('title', 'instructions')
    ordering = ('-created_at',)
    inlines = [RecipeIngredientInline, RecipeImageInline]


@admin.register(RecipeCollection)
class RecipeCollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'recipe_count')
    search_fields = ('title',)
    ordering = ('-id',)

    def recipe_count(self, obj):
        return obj.recipe_count()
    recipe_count.short_description = 'Number of Recipes'
