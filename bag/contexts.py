from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):
    
    bag_items = []
    total = Decimal('0.00')
    product_count = 0
    bag = request.session.get('bag', {})


    if bag_items:
        free_threshold = Decimal(str(settings.FREE_DELIVERY_THRESHOLD))
        if total < free_threshold:
            delivery = Decimal(str(settings.STANDARD_DELIVERY))
            free_delivery_delta = free_threshold - total
        else:
            delivery = Decimal('0.00')
            free_delivery_delta = Decimal('0.00')
    else:
        delivery = Decimal('0.00')
        free_delivery_delta = Decimal('0.00')

    grand_total = total + delivery

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context