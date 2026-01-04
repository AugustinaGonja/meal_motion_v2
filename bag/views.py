from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from products.models import Product


def shopping_bag(request):

    """
    View rendering shopping bag page.
    """

    return render(request, 'bag/shopping_bag.html')


def add_items(request, item_id):
    """ View quantity of indiviual items added to bag. """

    product = get_object_or_404(Product, pk=item_id)

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(
            request,
            f'Updated {product.name} quantity to {bag[item_id]}'
        )
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def update_bag(request, item_id):

    """
    View to update qty of items directly from the shopping bag.
    """

    quantity = int(request.POST.get('quantity', 1))
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id] = quantity
        messages.success(request, 'Item quantity updated.')
    else:
        bag.pop(item_id, None)
        messages.success(request, 'Item removed.')

    request.session['bag'] = bag
    return redirect(request.POST.get('redirect_url', 'shopping_bag'))


def remove_item(request, item_id):

    """
    View to remove item directly from the shopping bag.
    """

    bag = request.session.get('bag', {})
    bag.pop(item_id, None)

    messages.success(request, 'Item removed.')
    request.session['bag'] = bag
    return redirect(reverse('bag'))
