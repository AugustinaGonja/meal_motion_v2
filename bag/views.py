from django.shortcuts import render, redirect, reverse
from django.contrib import messages

# Create your views here.

def shopping_bag(request):
    
    """ 
    View rendering shopping bag page
     
    """

    return render(request, 'bag/shopping_bag.html')


def add_items(request, item_id):
    """ View quantity of indiviual items added to bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})
    
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)