from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import generic
from .forms import RecipeForm, RecipeSearchForm
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.http import HttpResponseForbidden
from comments.forms import CommentForm
from comments.models import Comment
from django.urls import reverse
from django.views.generic.edit import FormMixin
from valoraciones.forms import RatingForm
from valoraciones.models import Rating
# Create your views here.

class RecipesList(generic.ListView):
    model = Recipe
    paginate_by = 3
    context_object_name = "recipes_list"
    template_name = "recetas/recipes.html"
    def get_queryset(self):
        queryset = Recipe.objects.order_by("-updated_at")
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = RecipeSearchForm(self.request.GET)
        return context
    
    
class DetailedRecipe(FormMixin,generic.DetailView):
    model = Recipe
    context_object_name = "detailed_recipe"
    template_name = "recetas/detailed_recipe.html"
    form_class = CommentForm

    def get_success_url(self):
        return reverse('recetas:recipe_detail', kwargs={'pk': self.object.pk, 'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(recipe=self.object)
        context['ratings'] = Rating.objects.filter(recipe=self.object)
        context['average_rating'] = self.object.average_rating()
        context['rating_count'] = self.object.rating_count()

        if self.request.user.is_authenticated:
            context['comment_form'] = self.get_form()
            context['rating_form'] = RatingForm()
        else:
            context['comment_form'] = None
            context['rating_form'] = None
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('usuarios:login')  # Redirect to login page if not authenticated
        self.object = self.get_object()
        
        if 'comment_submit' in request.POST:
            comment_form = self.get_form()
            if comment_form.is_valid():
                return self.form_valid(comment_form)
            else:
                return self.form_invalid(comment_form)
        elif 'rating_submit' in request.POST:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                new_rating = rating_form.save(commit=False)
                new_rating.recipe = self.object
                new_rating.user = self.request.user
                new_rating.save()
                return redirect(self.get_success_url())
            else:
                return self.form_invalid(rating_form)

    def form_valid(self, form):
        new_comment = form.save(commit=False)
        new_comment.recipe = self.object
        new_comment.user = self.request.user
        new_comment.save()
        return super().form_valid(form)

@login_required
def new_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('usuarios:profile')
    else:
        form = RecipeForm()
    return render(request,'recetas/create_recipe.html',{'form':form})


class MyRecipes(LoginRequiredMixin,generic.ListView):
    model = Recipe
    paginate_by = 3
    context_object_name = "recipes_list"
    template_name = "recetas/recipes.html"
    # def get_queryset(self):
    #     return Recipe.objects.filter(author=self.request.user).order_by("-updated_at")
    
    def get_queryset(self):
        queryset = Recipe.objects.filter(author=self.request.user).order_by("-updated_at")
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = RecipeSearchForm(self.request.GET)
        return context
    
@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            if recipe.title != Recipe.objects.get(pk=recipe.pk).title:
                recipe.slug = slugify(recipe.title)
            recipe.save()
            return redirect('usuarios:profile')
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recetas/create_recipe.html', {'form': form})

@login_required
def delete_recipe(request,recipe_id):
    recipe = get_object_or_404(Recipe,id=recipe_id)
    if recipe.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this recipe.")
    
    recipe.delete()
    return redirect('usuarios:profile')
    
