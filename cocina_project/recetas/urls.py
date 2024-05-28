from django.urls import path
from . import views
from .views import delete_recipe

# Create your urls here

app_name = 'recetas'
urlpatterns = [
    path('new_recipe/',views.new_recipe,name='new_recipe'),
    path('',views.RecipesList.as_view(),name='home'),
    path('recetas/<int:pk>/<slug:slug>/',views.DetailedRecipe.as_view(),name='recipe_detail'),
    path('my_recipes/',views.MyRecipes.as_view(),name='my_recipes'),
    path('recipe/edit/<int:recipe_id>',views.edit_recipe,name='edit_recipe'),
    path('recetas/delete/<int:recipe_id>',delete_recipe, name='delete_recipe')

]