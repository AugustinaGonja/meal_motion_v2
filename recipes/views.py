from django.shortcuts import render, get_object_or_404
from .models import Recipe, Category
from django.db.models.functions import Lower

# Create your views here.

def recipe_list(request):

    """
    Display list of recipes with filter, and sorting
    functionality.

    """
    recipes = Recipe.objects.all()
    total_recipes = recipes.count()
    categories_names = []
    category_objects = Category.objects.none()
    sort = None
    direction = None

    # Sorting
    if 'sort' in request.GET:
        sortkey = request.GET['sort']
        sort = sortkey
        if sortkey == 'name':
            sortkey = 'lower_name'
            recipes = recipes.annotate(lower_name=Lower("name"))

        if 'direction' in request.GET:
            direction = request.GET['direction']
            if direction == 'desc':
                sortkey = f'-{sortkey}'
        recipes = recipes.order_by(sortkey)
    current_sorting = f'{sort}_{direction}'

    # Filtering by category
    if 'category' in request.GET:
        categories_names = request.GET['category'].split(',')
        recipes = recipes.filter(categories__name__in=categories_names)
        category_objects = Category.objects.filter(name__in=categories_names)
        total_recipes = recipes.count()
        
    context = {
        'recipes' : recipes,
        'current_categories': categories_names,
        'category_objects': category_objects,
        'current_sorting': sort,
        'total_recipes':total_recipes,
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
