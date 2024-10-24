from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from .forms import SignUpForm  

User = get_user_model()

class SignUpViewTests(TestCase):

    def test_signup_success(self):
        """Test that a user can sign up successfully and is logged in."""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
        })

        form = SignUpForm(data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
        })

        self.assertEqual(User.objects.count(), 1, msg="User creation failed. Form errors: {}".format(form.errors))

        self.assertEqual(User.objects.get(username='newuser').username, 'newuser')

        self.assertRedirects(response, reverse('home'))
    
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_signup_invalid_form(self):
        """Test that the signup form does not accept invalid data."""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'securepassword123',
            'password2': 'differentpassword123',
        })

        self.assertEqual(User.objects.count(), 0)

        form = SignUpForm(response.wsgi_request.POST)
        self.assertFalse(form.is_valid())

        self.assertFalse(response.wsgi_request.user.is_authenticated)

        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_user_already_exists(self):
        """Test that the signup form does not accept existing usernames."""
        User.objects.create_user(username='existinguser', password='securepassword123')

        response = self.client.post(reverse('signup'), {
            'username': 'existinguser',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
        })

        self.assertEqual(User.objects.count(), 1)

        form = SignUpForm(response.wsgi_request.POST)
        self.assertFalse(form.is_valid())

        self.assertFalse(response.wsgi_request.user.is_authenticated)

        self.assertTemplateUsed(response, 'registration/signup.html')


class SignUpFormTests(TestCase):

    def test_signup_form_valid(self):
        """Test that the signup form is valid with correct data."""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_password_mismatch(self):
        """Test that the signup form is invalid when passwords do not match."""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'securepassword123',
            'password2': 'differentpassword123',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_signup_form_missing_fields(self):
        """Test that the signup form is invalid when required fields are missing."""
        form_data = {
            'username': '',
            'email': '',
            'password1': '',
            'password2': '',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password1', form.errors)

    def test_signup_form_email_field(self):
        """Test that the email field is required and valid."""
        form_data = {
            'username': 'newuser',
            'email': 'invalid-email',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_signup_form_username_already_exists(self):
        """Test that the signup form is invalid when the username already exists."""
        User.objects.create_user(username='existinguser', password='securepassword123', email='existinguser@example.com')

        form_data = {
            'username': 'existinguser',
            'email': 'newuser@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)