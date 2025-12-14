from django.shortcuts import render
from .models import Recipe

# Create your views here.

def recipe_list(request):

    """
    Display list of recipes with search, filter, and sorting
    functionality.

    """
    recipes = Recipe.objects.all()

    context = {
        'recipes' : recipes
    }

    return render(request, 'recipes/recipes.html', context)
