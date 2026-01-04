from django.shortcuts import render, get_object_or_404

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order

# Create your views here.


@login_required
def profile(request):
    """Display and update user profile."""

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
        else:
            messages.error(
                request,
                'Profile not updated. Please ensure the form is valid.'
            )

    form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)


def order_history(request, order_number):
    """Display a past order."""
    order = get_object_or_404(Order, order_number=order_number)

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
        }

    return render(request, template, context)
