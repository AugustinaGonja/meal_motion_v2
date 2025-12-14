from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.

def product_list(request):

    """
    Display list of products with search, filter, and sorting
    functionality.

    """
    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)


def product_details(request, product_id):

    """
    Display a specific product's details.
    
    """
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'products/product_details.html', context)