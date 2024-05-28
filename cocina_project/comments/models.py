from django.db import models
from django.contrib.auth.models import User
from recetas.models import Recipe
from usuarios.models import Profile
# Create your models here.

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.recipe.title}"
    
    def profile_picture_url(self):
        # Access the related Profile instance
        profile = Profile.objects.get(user=self.user)
        # Return the profile picture URL
        return profile.profile_picture.url if profile.profile_picture else None
