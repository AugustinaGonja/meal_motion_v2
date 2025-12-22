from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .models import Order, OrderLineItem
from products.models import Product

from .forms import OrderForm
from bag.contexts import bag_contents

import stripe # type: ignore
import json

# Create your views here.

@require_POST
def cache_checkout_data(request):

    """
    Cache checkout data in Stripe PaymentIntent metadata.
    
    """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(
            pid,
            metadata={
                'bag': json.dumps(request.session.get('bag', {})),
                'save_info': request.POST.get('save_info'),
                'username': request.user,
            }
        )
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(
            request,
            'Sorry, your payment cannot be processed right now.'
        )
        return HttpResponse(content=str(e), status=400)
    
def checkout(request):

    """
    A view to handle the checkout page functionality.

    """
    stripe.secret_key = settings.STRIPE_SECRET_KEY
    stripe_public_key = settings.STRIPE_PUBLIC_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'contact_number': request.POST['contact_number'],
            'town_or_city': request.POST['town_or_city'],
            'address_line_1': request.POST['address_line_1'],
            'address_line_2': request.POST['address_line_2'],
            'post_code': request.POST['post_code'],
            'county': request.POST['county'],
            'country': request.POST['country'],
        }

        order_form = OrderForm(form_data)
        
        if order_form.is_valid():
            order = order_form.save()

            bag_items = bag_contents(request)['bag_items']

            for item in bag_items:
                product = Product.objects.get(id=item['item_id'])
                quantity = item['quantity']

                OrderLineItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                )

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(
                request,
                'There is an error in your form. Check your information and try again.'
            )
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There are currently no items in your bag.")
            return redirect(reverse('products'))
    
    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe.secret_key

    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )
    
    order_form = OrderForm()
    
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        }

    return render(request, template, context)

def checkout_success(request, order_number):

    """
    A view to handle successful checkouts.
    
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    messages.success(
        request,
        f'Order successfully processed! Your order number is {order_number}. A confirmation email will be sent to {order.email}.'
    )

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)