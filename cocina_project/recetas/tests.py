from django.test import TestCase
from django.contrib.auth.models import User
from .models import Recipe, Category
from django.core.exceptions import ValidationError
# Create your tests here.

class RecipeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.category = Category.objects.create(name='Test Category')

    def test_duplicate_recipe(self):
        # Create the first recipe
        Recipe.objects.create(
            title='Test Recipe',
            description='Test Description',
            preparation_time=1,
            ingredients='Test Ingredients',
            steps='Test Steps',
            author=self.user,
            category = self.category
        )

        # Attempt to create a duplicate recipe
        duplicate_recipe = Recipe(
            title='Test Recipe',
            description='Another Test Description',
            preparation_time=2,
            ingredients='More Test Ingredients',
            steps='More Test Steps',
            author=self.user,
            category=self.category
        )

        # Verify that validation error is raised
        with self.assertRaises(ValidationError):
            duplicate_recipe.save()