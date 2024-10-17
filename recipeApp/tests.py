from django.test import TestCase
from django.contrib.auth.models import User
from .models import Recipe, RecipeIngredient, RecipeCollection, RecipeImage
from datetime import timedelta
from django.urls import reverse


class RecipeModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Test Recipe',
            servings=4,
            prepration_time=timedelta(minutes=20),  
            total_time=timedelta(minutes=45),     
            calories=200,
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
        self.assertEqual(self.recipe.prepration_time, timedelta(minutes=20))
        self.assertEqual(self.recipe.total_time, timedelta(minutes=45))
        self.assertEqual(self.recipe.calories, 200)
        self.assertEqual(self.recipe.instructions, "Test instructions")
        self.assertEqual(self.recipe.featured, True)
        self.assertEqual(self.recipe.cuisine, Recipe.CuisineType.SOUTH_INDIAN)
        self.assertEqual(self.recipe.food_type, Recipe.FoodType.VEGAN)
        self.assertEqual(self.recipe.difficulty, Recipe.DifficultyLevel.EASY)

    def test_get_total_ingredients(self):
        """Test if the method returns the correct number of ingredients."""
        self.assertEqual(self.recipe.get_total_ingredients(), 0)  

    def test_recipe_string_representation(self):
        """Test the string representation of the recipe."""
        self.assertEqual(str(self.recipe), 'Test Recipe')


class RecipeImageModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.recipe = Recipe.objects.create(
            author=self.user,
            title="Test Recipe",
            servings=4,
            prepration_time=timedelta(minutes=20),
            total_time=timedelta(minutes=45),
            calories=200,
            instructions="Test instructions for the recipe.",
            featured=True,
            cuisine=Recipe.CuisineType.SOUTH_INDIAN,
            food_type=Recipe.FoodType.VEGETARIAN,
            difficulty=Recipe.DifficultyLevel.EASY
        )

    def test_recipe_image_creation(self):
        """Test that RecipeImage can be added to a Recipe."""
        image = RecipeImage.objects.create(
            recipe=self.recipe,
            image="path/to/image.jpg",
            description="Sample description for image"
        )
        self.assertEqual(self.recipe.images.count(), 1)
        self.assertEqual(str(image), f"Image for {self.recipe.title}")
        self.assertEqual(image.description, "Sample description for image")
    
    def test_image_string_representation(self):
        """Test the string representation of the image."""
        self.assertEqual(str(self.recipe.title), 'Test Recipe')
        
        
class RecipeIngredientModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Test Recipe',
            servings=4,
            prepration_time=timedelta(minutes=30),
            total_time=timedelta(minutes=45),
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


# view testing

class HomePageViewTests(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))  
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')


class RecipeListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.recipes = [
            Recipe.objects.create(
                author=self.user,
                title='Recipe 1',
                servings=4,
                prepration_time=timedelta(minutes=30),
                total_time=timedelta(minutes=40),
                calories=300,
                instructions='Instructions for Recipe 1.',
                featured=False,
                cuisine=Recipe.CuisineType.NORTH_INDIAN,
                food_type=Recipe.FoodType.VEGETARIAN,
                difficulty=Recipe.DifficultyLevel.EASY
            ),
            Recipe.objects.create(
                author=self.user,
                title='Recipe 2',
                servings=2,
                prepration_time=timedelta(minutes=30),
                total_time=timedelta(minutes=40),
                calories=200,
                instructions='Instructions for Recipe 2.',
                featured=True,
                cuisine=Recipe.CuisineType.SOUTH_INDIAN,
                food_type=Recipe.FoodType.VEGAN,
                difficulty=Recipe.DifficultyLevel.MEDIUM
            )
        ]

    def test_recipe_list_view_status_code(self):
        response = self.client.get(reverse('recipe_list'))  
        self.assertEqual(response.status_code, 200)

    def test_recipe_list_view_template(self):
        response = self.client.get(reverse('recipe_list'))
        self.assertTemplateUsed(response, 'recipes/list.html')

    def test_recipe_list_view_context(self):
        response = self.client.get(reverse('recipe_list'))
        self.assertIn('recipes', response.context)
        self.assertEqual(len(response.context['recipes']), 1)  


class RecipeCollectionListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.collection = RecipeCollection.objects.create(
            title='Collection 1',
            user=self.user
        )

    def test_collection_list_view_status_code(self):
        response = self.client.get(reverse('collection_list'))  
        self.assertEqual(response.status_code, 200)

    def test_collection_list_view_template(self):
        response = self.client.get(reverse('collection_list'))
        self.assertTemplateUsed(response, 'collections/list.html')

    def test_collection_list_view_context(self):
        response = self.client.get(reverse('collection_list'))
        self.assertIn('collections', response.context)
        self.assertEqual(len(response.context['collections']), 1)


class RecipeDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Recipe 1',
            servings=4,
            prepration_time=timedelta(minutes=30),
            total_time=timedelta(minutes=40),
            calories=300,
            instructions='Instructions for Recipe 1.',
            featured=False,
            cuisine=Recipe.CuisineType.NORTH_INDIAN,
            food_type=Recipe.FoodType.VEGETARIAN,
            difficulty=Recipe.DifficultyLevel.EASY
        )

    def test_recipe_detail_view_status_code(self):
        response = self.client.get(reverse('recipe_detail', args=[self.recipe.pk]))  
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view_template(self):
        response = self.client.get(reverse('recipe_detail', args=[self.recipe.pk]))
        self.assertTemplateUsed(response, 'recipes/detail.html')


class RecipeCollectionDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.collection = RecipeCollection.objects.create(
            title='Collection 1',
            user=self.user
        )
        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Recipe 1',
            servings=4,
            prepration_time=timedelta(minutes=30),
            total_time=timedelta(minutes=40),
            calories=300,
            instructions='Instructions for Recipe 1.',
            featured=False,
            cuisine=Recipe.CuisineType.NORTH_INDIAN,
            food_type=Recipe.FoodType.VEGETARIAN,
            difficulty=Recipe.DifficultyLevel.EASY
        )
        self.collection.recipes.add(self.recipe)

    def test_collection_detail_view_status_code(self):
        response = self.client.get(reverse('collection_detail', args=[self.collection.pk]))  
        self.assertEqual(response.status_code, 200)

    def test_collection_detail_view_template(self):
        response = self.client.get(reverse('collection_detail', args=[self.collection.pk]))
        self.assertTemplateUsed(response, 'collections/detail.html')
