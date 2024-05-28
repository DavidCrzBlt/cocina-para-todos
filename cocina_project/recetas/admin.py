from django.contrib import admin
from .models import Recipe

# Register your models here.
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title','description','ingredients','steps','preparation_time',
                    'image','category','author','created_at','updated_at']
    prepopulated_fields = {"slug": ["title"]}

admin.site.register(Recipe,RecipeAdmin)