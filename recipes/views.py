from django.shortcuts import render, get_object_or_404
from .models import Recipe, Category

# Create your views here.

def recipe_list(request):

    """
    Display list of recipes with search, filter, and sorting
    functionality.

    """
    recipes = Recipe.objects.all()
    categories_names = []
    category_objects = Category.objects.none()

    # Filtering by category
    if 'category' in request.GET:
        categories_names = request.GET['category'].split(',')
        recipes = recipes.filter(categories__name__in=categories_names)
        category_objects = Category.objects.filter(name__in=categories_names)

    context = {
        'recipes' : recipes,
        'current_categories': categories_names,
        'category_objects': category_objects,
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
