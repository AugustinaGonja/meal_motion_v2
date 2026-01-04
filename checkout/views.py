from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import HttpResponse

from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile
from .forms import OrderForm
from profiles.forms import UserProfileForm
from bag.contexts import bag_contents

import stripe
import json

@require_POST
def cache_checkout_data(request):
    """Cache checkout data in Stripe PaymentIntent metadata."""
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(
            pid,
            metadata={
                'bag': json.dumps(request.session.get('bag', {})),
                'save_info': request.POST.get('save_info'),
                'username': request.user.username if request.user.is_authenticated else 'anonymous',
            }
        )
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be processed right now.')
        return HttpResponse(content=str(e), status=400)


def checkout(request):
    """View to handle the checkout page functionality."""

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_public_key = settings.STRIPE_PUBLIC_KEY

    bag = request.session.get('bag', {})

    if not bag:
        messages.error(request, "There are currently no items in your bag.")
        return redirect(reverse('products'))

    if request.method == 'POST':
        form_data = {key: request.POST.get(key, '') for key in [
            'full_name', 'email', 'contact_number', 'town_or_city',
            'address_line_1', 'address_line_2', 'post_code', 'county', 'country'
        ]}
        order_form = OrderForm(form_data)

        if order_form.is_valid():
            order = order_form.save()
            bag_items = bag_contents(request)['bag_items']

            for item in bag_items:
                try:
                    product = Product.objects.get(id=item['item_id'])
                    OrderLineItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item['quantity'],
                    )
                except Product.DoesNotExist:
                    messages.error(request, f"Product {item['item_id']} not found in database.")

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, "There is an error in your form. Check your information and try again.")
    else:
        # GET request: prepare form with initial data
        initial_data = {}
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                initial_data = {
                    'full_name': request.user.get_full_name() or '',
                    'email': request.user.email or '',
                    'contact_number': profile.default_contact_number or '',
                    'country': profile.default_country or '',
                    'post_code': profile.default_post_code or '',
                    'town_or_city': profile.default_town_or_city or '',
                    'address_line_1': profile.default_address_line_1 or '',
                    'address_line_2': profile.default_address_line_2 or '',
                    'county': profile.default_county or '',
                }
            except UserProfile.DoesNotExist:
                profile = None

        try:
            order_form = OrderForm(initial=initial_data)
        except Exception as e:
            print("DEBUG: OrderForm initialization failed:", e)
            order_form = OrderForm()

    # Stripe PaymentIntent
    total = bag_contents(request)['grand_total']
    stripe_total = round(total * 100)

    try:
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
    except Exception as e:
        messages.error(request, f"Stripe error: {e}")
        intent = None

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret if intent else None,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """View to handle successful checkouts."""
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            order.user_profile = profile
            order.save()

            if save_info:
                profile_data = {
                    'default_contact_number': order.contact_number,
                    'default_country': order.country,
                    'default_post_code': order.post_code,
                    'default_town_or_city': order.town_or_city,
                    'default_address_line_1': order.address_line_1,
                    'default_address_line_2': order.address_line_2,
                    'default_county': order.county,
                }
                user_profile_form = UserProfileForm(profile_data, instance=profile)
                if user_profile_form.is_valid():
                    user_profile_form.save()
        except UserProfile.DoesNotExist:
            pass  # user has no profile, skip

    messages.success(
        request,
        f'Order successfully processed! Your order number is {order_number}. A confirmation email will be sent to {order.email}.'
    )

    request.session.pop('bag', None)

    return render(request, 'checkout/checkout_success.html', {'order': order})
