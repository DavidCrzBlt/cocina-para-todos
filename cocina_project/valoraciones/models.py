from django.db import models
from usuarios.models import User
from recetas.models import Recipe
# Create your models here.

class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()  # Puede ser de 1 a 5, por ejemplo
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('recipe', 'user')  # Para asegurarse de que un usuario pueda valorar una receta solo una vez

    def __str__(self):
        return f"Rating {self.score} by {self.user.username} for {self.recipe.title}"
