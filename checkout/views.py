from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages

from .forms import OrderForm

# Create your views here.

def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There are currently no items in your bag.")
        return redirect(reverse('products'))
    
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51SfP06LGKKegfF9bNcMUzw1ynGXwgAOiAVkqfRX1qMkCX1ukUq48KakQ2KXS2fmJYGghy5ESQcxoEz6ZOGejEKLU00DhSan49Q',
        'client_secret': 'test.client_secret',
        }

    return render(request, template, context)