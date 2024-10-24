import os
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Recipe, RecipeIngredient, RecipeCollection, RecipeImage
from .forms import RecipeCollectionForm, RecipeForm, RecipeIngredientForm
from datetime import timedelta
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .filters import RecipeFilter, RecipeCollectionFilter


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
        self.assertEqual(len(response.context['recipes']), 2)  


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
        self.client.login(username='testuser', password='testpass')
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
    
    def test_login_required_for_recipe_detail_view(self):
        """Test that login is required to access the recipe detail view."""
        self.client.logout()
        response = self.client.get(reverse('recipe_detail', args=[self.recipe.pk]))
        self.assertRedirects(response, f"/account/login/?next=/recipes/{self.recipe.pk}/")


class RecipeCollectionDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
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
    
    def test_login_required_for_recipe_collection_detail_view(self):
        """Test that login is required to access the recipe collection detail view."""
        self.client.logout()
        response = self.client.get(reverse('collection_detail', args=[self.collection.pk]))
        self.assertRedirects(response, f"/account/login/?next=/collections/{self.collection.pk}/")


class RecipeCollectionCreateViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_create_collection_valid(self):
        response = self.client.post(reverse('collection_create'), {
            'title': 'My Recipe Collection',
            'recipes': [1, 2], 
        })
        self.assertEqual(response.status_code, 200) 

    def test_create_collection_invalid(self):
        response = self.client.post(reverse('collection_create'), {
            'title': '', 
        })
        self.assertEqual(response.status_code, 200)  
        
    def test_login_required_for_collection_create_view(self):
        """Test that login is required to access the recipe collection create view."""
        self.client.logout()  
        response = self.client.get(reverse('collection_create'))
        self.assertRedirects(response, "/account/login/?next=/collections/create/")  
        
        
class RecipeCollectionUpdateViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.collection = RecipeCollection.objects.create(title='Old Title', user=self.user)

    def test_update_collection_valid(self):
        response = self.client.post(reverse('collection_edit', kwargs={'pk': self.collection.pk}), {
            'title': 'Old Title',
            'recipes': [1],  
        })
        self.assertEqual(response.status_code, 200)  
        self.collection.refresh_from_db()
        self.assertEqual(self.collection.title, 'Old Title')

    def test_update_collection_invalid(self):
        response = self.client.post(reverse('collection_edit', kwargs={'pk': self.collection.pk}), {
            'title': '',  
        })
        self.assertEqual(response.status_code, 200)  
        
    def test_collection_owner_required_for_collection_update_view(self):
        """Test that only the collection owner can access the collection update view."""
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        
        self.client.login(username='otheruser', password='otherpass')
        response = self.client.get(reverse('collection_edit', kwargs={'pk': self.collection.pk}))
        self.assertEqual(response.status_code, 403)  # Forbidden

        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('collection_edit', kwargs={'pk': self.collection.pk}))
        self.assertEqual(response.status_code, 200)  # Allowed


class RecipeCreateViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_create_recipe_valid(self):
        response = self.client.post(reverse('recipe-create'), {
            'title': 'New Recipe',
            'servings': 4,
            'prepration_time': timedelta(minutes=20),
            'total_time': timedelta(minutes=20),
            'calories': 500,
            'instructions': 'Mix all ingredients.',
            'cuisine': 1,  
            'food_type': 1,  
            'difficulty': 1,  
            'ingredients-0-name': 'Sugar',
            'ingredients-0-quantity': 100,
            'ingredients-0-unit': 1,  
            'images-0-image': SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Recipe.objects.filter(title='New Recipe').exists())

    def test_create_recipe_invalid(self):
        response = self.client.post(reverse('recipe-create'), {
            'title': '',  # Invalid title
        })
        self.assertEqual(response.status_code, 200)  
    
    def test_login_required_for_recipe_create_view(self):
        """Test that login is required to access the recipe create view."""
        self.client.logout()  
        response = self.client.get(reverse('recipe-create'))
        self.assertRedirects(response, "/account/login/?next=/recipes/create/")


class RecipeUpdateViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Old Recipe',
            servings=4,
            prepration_time=timedelta(minutes=20),
            total_time=timedelta(minutes=20),
            calories=500,
            instructions='Mix all ingredients.',
            cuisine=Recipe.CuisineType.NORTH_INDIAN,
            food_type=Recipe.FoodType.VEGETARIAN,
            difficulty=Recipe.DifficultyLevel.EASY
        )

    def test_update_recipe_valid(self):
        response = self.client.post(reverse('recipe_edit', kwargs={'pk': self.recipe.pk}), {
            'title': 'Old Recipe',
            'servings': 4,
            'prepration_time': timedelta(minutes=20),
            'total_time': timedelta(minutes=20),
            'calories': 500,
            'instructions': 'Mix all ingredients.',
            'cuisine': 1,  
            'food_type': 1,  
            'difficulty': 1,  
        })
        self.assertEqual(response.status_code, 302)  
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, 'Old Recipe')

    def test_update_recipe_invalid(self):
        response = self.client.post(reverse('recipe_edit', kwargs={'pk': self.recipe.pk}), {
            'title': '', 
        })
        self.assertEqual(response.status_code, 200)  
    
    def test_recipe_owner_required_for_recipe_update_view(self):
        """Test that only the recipe owner can access the recipe update view."""
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
    
        self.client.login(username='otheruser', password='otherpass')
        response = self.client.get(reverse('recipe_edit', kwargs={'pk': self.recipe.pk}))
        self.assertEqual(response.status_code, 403)  # Forbidden

        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('recipe_edit', kwargs={'pk': self.recipe.pk}))
        self.assertEqual(response.status_code, 200)  # Allowed


class RecipeDeleteViewTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            author=self.user,
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

    def test_delete_recipe_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('recipe_delete', args=[self.recipe.pk]))

        self.assertFalse(Recipe.objects.filter(pk=self.recipe.pk).exists())
        self.assertRedirects(response, reverse('recipe_list'))
    
    def test_recipe_owner_required_for_recipe_delete_view(self):
        """Test that only the recipe owner can access the recipe delete view."""
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        self.client.login(username='otheruser', password='otherpass')
        response = self.client.get(reverse('recipe_delete', args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 403)  # Forbidden

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('recipe_delete', args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 200)  # Allowed


class RecipeCollectionDeleteViewTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        self.collection = RecipeCollection.objects.create(
            title='Test Collection',
            user=self.user,
        )

    def test_delete_collection_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('collection_delete', args=[self.collection.pk]))

        self.assertFalse(RecipeCollection.objects.filter(pk=self.collection.pk).exists())
        self.assertRedirects(response, reverse('collection_list'))
    
    def test_collection_owner_required_for_collection_delete_view(self):
        """Test that only the collection owner can access the collection delete view."""
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        
        # Test access by a different user
        self.client.login(username='otheruser', password='otherpass')
        response = self.client.get(reverse('collection_delete', args=[self.collection.pk]))
        self.assertEqual(response.status_code, 403)  # Forbidden

        # Test access by the collection owner
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('collection_delete', args=[self.collection.pk]))
        self.assertEqual(response.status_code, 200)  # Allowed


# Form Test
class RecipeFormTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.recipe_data = {
            'title': 'Test Recipe',
            'servings': 4,
            'prepration_time': timedelta(hours=1, minutes=30),
            'total_time': timedelta(hours=2),
            'calories': 500,
            'instructions': "Step 1.\nStep 2.",
            'cuisine': 1,  
            'food_type': 1,
            'difficulty': 1,
            'featured': True,
        }

    def test_valid_recipe_form(self):
        form = RecipeForm(data=self.recipe_data)
        self.assertTrue(form.is_valid())

    def test_blank_instruction_lines(self):
        self.recipe_data['instructions'] = "Step 1.\n\n\nStep 2."
        form = RecipeForm(data=self.recipe_data)
        self.assertFalse(form.is_valid())
        self.assertIn('instructions', form.errors)

    def test_preparation_time_less_than_total_time(self):
        self.recipe_data['prepration_time'] = timedelta(hours=2, minutes=30)
        form = RecipeForm(data=self.recipe_data)
        self.assertFalse(form.is_valid())
        self.assertIn('prepration_time', form.errors)

    def test_invalid_duration_format(self):
        self.recipe_data['prepration_time'] = 'Invalid format'
        form = RecipeForm(data=self.recipe_data)
        self.assertFalse(form.is_valid())
        self.assertIn('prepration_time', form.errors)


class RecipeIngredientFormTests(TestCase):

    def test_valid_ingredient_form(self):
        form_data = {
            'name': 'Sugar',
            'quantity': 100,
            'unit': 1,  
            'optional': False
        }
        form = RecipeIngredientForm(data=form_data)
        self.assertTrue(form.is_valid())


class RecipeCollectionFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            servings=4,
            prepration_time=timedelta(hours=1, minutes=30),
            total_time=timedelta(hours=2),
            calories=500,
            instructions="Step 1.",
            author=self.user,
            cuisine=1,
            food_type=1,
            difficulty=1,
            featured=True,
        )

    def test_valid_collection_form(self):
        form_data = {
            'title': 'My Collection',
            'recipes': [self.recipe.pk],
        }
        form = RecipeCollectionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_collection_form_with_no_recipes(self):
        form_data = {
            'title': 'My Collection',
            'recipes': [],
        }
        form = RecipeCollectionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('recipes', form.errors)


#filter test
class RecipeFilterTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.recipe1 = Recipe.objects.create(
            author=cls.user,
            title='Vegetarian Pasta',
            cuisine=Recipe.CuisineType.CHINESE,
            servings=4,
            prepration_time=timedelta(hours=1, minutes=30),
            total_time=timedelta(hours=1, minutes=30),
            calories=300,
            instructions='Boil water and cook pasta.',
            featured=False,
            food_type=Recipe.FoodType.VEGAN,
            difficulty=Recipe.DifficultyLevel.EASY
        )
        cls.recipe2 = Recipe.objects.create(
            author=cls.user,
            title='Chicken Curry',
            cuisine=Recipe.CuisineType.CHINESE,
            servings=4,
            prepration_time=timedelta(hours=1, minutes=30),
            total_time=timedelta(hours=1, minutes=30),
            calories=500,
            instructions='Cook chicken with spices.',
            featured=False,
            food_type=Recipe.FoodType.VEGETARIAN,
            difficulty=Recipe.DifficultyLevel.EASY
        )
        cls.recipe3 = Recipe.objects.create(
            author=cls.user,
            title='Fried Rice',
            cuisine=Recipe.CuisineType.CHINESE,
            servings=4,
            prepration_time=timedelta(hours=1),
            total_time=timedelta(hours=1, minutes=30),
            calories=400,
            instructions='Stir fry rice with vegetables.',
            featured=False,
            food_type=Recipe.FoodType.VEGETARIAN,
            difficulty=Recipe.DifficultyLevel.MEDIUM
        )

    def test_search_by_title(self):
        filter_set = RecipeFilter(data={'search': 'Vegetarian'}, queryset=Recipe.objects.all())
        self.assertEqual(len(filter_set.qs), 1)
        self.assertEqual(filter_set.qs.first(), self.recipe1)

    def test_search_by_author(self):
        filter_set = RecipeFilter(data={'search': 'testuser'}, queryset=Recipe.objects.all())
        self.assertEqual(len(filter_set.qs), 3)
    
    def test_search_by_cuisine(self):
        filter_set = RecipeFilter(data={'search': 'Chinese'}, queryset=Recipe.objects.all())
        self.assertEqual(len(filter_set.qs), 3)

    def test_filter_by_cuisine(self):
        filter_set = RecipeFilter(data={'cuisine': Recipe.CuisineType.CHINESE}, queryset=Recipe.objects.all())
        self.assertEqual(len(filter_set.qs), 3)  

    def test_filter_by_food_type(self):
        filter_set = RecipeFilter(data={'food_type': Recipe.FoodType.VEGETARIAN}, queryset=Recipe.objects.all())
        self.assertEqual(len(filter_set.qs), 2)  
        
    def test_filter_by_difficulty(self):
        filter_set = RecipeFilter(data={'difficulty': Recipe.DifficultyLevel.EASY}, queryset=Recipe.objects.all())
        self.assertEqual(len(filter_set.qs), 2)  

    def test_no_results(self):
        filter_set = RecipeFilter(data={'search': 'Non-existent'}, queryset=Recipe.objects.all())
        self.assertEqual(len(filter_set.qs), 0)

    def test_show_my_items(self):
        filter_set = RecipeFilter(data={'user_filter': True}, queryset=Recipe.objects.all(), user=self.user)
        self.assertEqual(len(filter_set.qs), 3)  


class RecipeCollectionFilterTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.recipe1 = Recipe.objects.create(
            author=cls.user,
            title='Vegetarian Pasta',
            cuisine=Recipe.CuisineType.CHINESE,
            servings=4,
            prepration_time=timedelta(hours=2),
            total_time=timedelta(hours=2),
            calories=300,
            instructions='Boil water and cook pasta.',
            featured=False,
            food_type=Recipe.FoodType.VEGETARIAN,
            difficulty=Recipe.DifficultyLevel.EASY
        )
        cls.recipe2 = Recipe.objects.create(
            author=cls.user,
            title='Chicken Curry',
            cuisine=Recipe.CuisineType.CHINESE,
            servings=4,
            prepration_time=timedelta(hours=2),
            total_time=timedelta(hours=2),
            calories=500,
            instructions='Cook chicken with spices.',
            featured=False,
            food_type=Recipe.FoodType.VEGETARIAN,
            difficulty=Recipe.DifficultyLevel.EASY
        )
        cls.collection = RecipeCollection.objects.create(
            title='My Favorite Recipes',
            user=cls.user
        )
        cls.collection.recipes.add(cls.recipe1)
        cls.collection.recipes.add(cls.recipe2)

    def test_search_by_collection_title(self):
        filter_set = RecipeCollectionFilter(data={'search': 'Favorite'}, queryset=RecipeCollection.objects.all())
        self.assertEqual(len(filter_set.qs), 1)
        self.assertEqual(filter_set.qs.first(), self.collection)

    def test_search_by_recipe_title(self):
        filter_set = RecipeCollectionFilter(data={'search': 'Pasta'}, queryset=RecipeCollection.objects.all())
        self.assertEqual(len(filter_set.qs), 1)
        self.assertEqual(filter_set.qs.first(), self.collection)

    def test_search_by_user(self):
        filter_set = RecipeCollectionFilter(data={'search': 'testuser'}, queryset=RecipeCollection.objects.all())
        self.assertEqual(len(filter_set.qs), 1)

    def test_no_results(self):
        filter_set = RecipeCollectionFilter(data={'search': 'Non-existent'}, queryset=RecipeCollection.objects.all())
        self.assertEqual(len(filter_set.qs), 0)
    
    def test_show_my_items(self):
        filter_set = RecipeCollectionFilter(data={'user_filter': True}, queryset=RecipeCollection.objects.all(), user=self.user)
        self.assertEqual(len(filter_set.qs), 1)
        self.assertEqual(filter_set.qs.first(), self.collection)