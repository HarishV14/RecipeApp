from django.test import TestCase
from django.contrib.auth.models import User
from .models import Recipe, RecipeIngredient, RecipeCollection
from datetime import timedelta


class RecipeModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Test Recipe',
            image='test_image.jpg',
            servings=4,
            prepration_time=timedelta(minutes=30),  
            total_time=timedelta(minutes=30),     
            calories=500,
            instructions='Test instructions',
            featured=True,
            cuisine=Recipe.CuisineType.SOUTH_INDIAN,
            food_type=Recipe.FoodType.VEGAN,
            difficulty=Recipe.DifficultyLevel.EASY,
        )

    def test_recipe_creation(self):
        """Test if the recipe was created correctly."""
        self.assertEqual(self.recipe.title, 'Test Recipe')
        self.assertEqual(self.recipe.servings, 4)
        self.assertTrue(self.recipe.featured)

    def test_get_total_ingredients(self):
        """Test if the method returns the correct number of ingredients."""
        self.assertEqual(self.recipe.get_total_ingredients(), 0)  

    def test_recipe_string_representation(self):
        """Test the string representation of the recipe."""
        self.assertEqual(str(self.recipe), 'Test Recipe')


class RecipeIngredientModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Test Recipe',
            image='test_image.jpg',
            servings=4,
            prepration_time=timedelta(minutes=30),
            total_time=timedelta(minutes=30),
            calories=500,
            instructions='Test instructions',
            featured=True,
            cuisine=Recipe.CuisineType.SOUTH_INDIAN,
            food_type=Recipe.FoodType.VEGAN,
            difficulty=Recipe.DifficultyLevel.EASY,
        )
        self.ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            name='Salt',
            quantity=1,
            unit=RecipeIngredient.UnitType.GRAMS, 
            optional=False
        )

    def test_ingredient_creation(self):
        """Test if the ingredient was created correctly."""
        self.assertEqual(self.ingredient.name, 'Salt')
        self.assertEqual(self.ingredient.quantity, 1)
        self.assertEqual(self.ingredient.unit, RecipeIngredient.UnitType.GRAMS)

    def test_ingredient_string_representation(self):
        """Test the string representation of the ingredient."""
        self.assertEqual(str(self.ingredient), '1 gms of Salt')


class RecipeCollectionModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.collection = RecipeCollection.objects.create(
            title='My Recipe Collection',
            user=self.user
        )
        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Test Recipe',
            image='test_image.jpg',
            servings=4,
            prepration_time=timedelta(minutes=30),
            total_time=timedelta(minutes=30),
            calories=500,
            instructions='Test instructions',
            featured=True,
            cuisine=Recipe.CuisineType.SOUTH_INDIAN,
            food_type=Recipe.FoodType.VEGAN,
            difficulty=Recipe.DifficultyLevel.EASY,
        )
        self.collection.recipes.add(self.recipe)

    def test_collection_creation(self):
        """Test if the recipe collection was created correctly."""
        self.assertEqual(self.collection.title, 'My Recipe Collection')
        self.assertEqual(self.collection.recipe_count(), 1)  

    def test_collection_string_representation(self):
        """Test the string representation of the collection."""
        self.assertEqual(str(self.collection), 'My Recipe Collection (1 recipes)')

