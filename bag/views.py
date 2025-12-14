from django.shortcuts import render, redirect, reverse
from django.contrib import messages

# Create your views here.

def shopping_bag(request):
    
    """ 
    View rendering shopping bag page
     
    """

    return render(request, 'bag/shopping_bag.html')