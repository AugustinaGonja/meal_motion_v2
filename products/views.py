from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Product

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm

# Create your views here.


def product_list(request):

    """
    Display list of products with search, filter, and sorting
    functionality.

    """
    products = Product.objects.all()
    total_products = products.count()
    query = None
    category_names = []
    category_objects = Category.objects.none()
    sort = None
    direction = None

    # Sorting
    if 'sort' in request.GET:
        sortkey = request.GET['sort']
        sort = sortkey
        if sortkey == 'name':
            sortkey = 'lower_name'
            products = products.annotate(lower_name=Lower("name"))

        if 'direction' in request.GET:
            direction = request.GET['direction']
            if direction == 'desc':
                sortkey = f'-{sortkey}'
        products = products.order_by(sortkey)

    # Filtering by category
    if 'category' in request.GET:
        category_names = request.GET['category'].split(',')
        products = products.filter(category__name__in=category_names)
        category_objects = Category.objects.filter(name__in=category_names)
        total_products = products.count()

    # Searching
    if 'q' in request.GET:
        query = request.GET.get('q')
        if not query:
            messages.error(request, "You didn't enter any search criteria!")
            return redirect(reverse('products'))

        queries = Q(name__icontains=query) | Q(description__icontains=query)
        products = products.filter(queries)
        total_products = products.count()

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'total_products': total_products,
        'search_term': query,
        'current_categories': category_names,
        'category_objects': category_objects,
        'current_sorting': sort,
    }

    return render(request, 'products/products.html', context)


def product_details(request, product_id):

    """
    Display a specific product's details.
    """
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'products/product_details.html', context)


@login_required
def add_product(request):
    """Add a product to the store."""

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added a product!')
            return redirect(reverse('product_details', args=[product.id]))
        else:
            messages.error(request, 'Product not added. Please try again.')

    form = ProductForm()
    template = 'products/add_product.html'
    context = {'form': form}

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """Edit an existing product in the store."""

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product.')
            return redirect(reverse('product_details', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Try again.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {'form': form, 'product': product}

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """Delete a product from the store."""

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted.')

    return redirect(reverse('products'))
