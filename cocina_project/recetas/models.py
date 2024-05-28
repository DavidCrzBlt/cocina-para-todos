from django.db import models
from categories.models import Category
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError

# Create your models here.


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()
    steps = models.TextField()
    preparation_time = models.FloatField()
    image = models.ImageField(upload_to='recipe_images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(default="", null=False)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if Recipe.objects.filter(title=self.title, author=self.author).exists():
            raise ValidationError('You have already published a recipe with this title.')
        super().save(*args, **kwargs)

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return sum(rating.score for rating in ratings) / ratings.count()
        return 0

    def rating_count(self):
        return self.ratings.count()