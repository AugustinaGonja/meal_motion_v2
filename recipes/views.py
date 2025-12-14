from django.shortcuts import render, get_object_or_404
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


def recipe_details(request, recipe_id):
    """ 
    View to display a specific recipe's details. 
    
    """

    recipe = get_object_or_404(Recipe, pk=recipe_id)

    context = {
        'recipe': recipe,
    }

    return render(request, 'recipes/recipe_details.html', context)
