from django.shortcuts import render, redirect, reverse
from django.contrib import messages

# Create your views here.

def shopping_bag(request):
    
    """ 
    View rendering shopping bag page.
     
    """

    return render(request, 'bag/shopping_bag.html')


def add_items(request, item_id):
    """ View quantity of indiviual items added to bag. """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})
    
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    request.session['bag'] = bag
    return redirect(redirect_url)

def update_bag(request, item_id):

    """ 
    View to update qty of items directly from the shopping bag. 
    
    """

    quantity = int(request.POST.get('quantity', 1))
    bag = request.session.get('bag', {})
    
    if quantity > 0 :
        bag[item_id] = quantity
        messages.success(request, 'Item quantity updated.')
    else:
        bag.pop(item_id, None)
        messages.success(request , 'Item removed.')

    request.session['bag'] = bag
    return redirect(request.POST.get('redirect_url', 'shopping_bag'))
