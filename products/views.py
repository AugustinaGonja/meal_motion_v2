from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Product
from django.contrib import messages
from django.db.models import Q

from .models import Product

# Create your views here.

def product_list(request):

    """
    Display list of products with search, filter, and sorting
    functionality.

    """
    products = Product.objects.all()
    query = None

    # Searching
    if request.GET:
        if 'q' in request.GET:
            query = request.GET.get('q')
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
    }

    return render(request, 'products/products.html', context)


def product_details(request, product_id):

    """
    Display a specific product's details.
    
    """
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'products/product_details.html', context)