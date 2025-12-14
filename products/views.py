from django.shortcuts import render
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
