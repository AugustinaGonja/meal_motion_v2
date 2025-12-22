import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from products.models import Product
from profiles.models import UserProfile

# Create your models here.

class Order(models.Model):
    order_number = models.CharField(max_length=50, unique=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True , blank = True, related_name='orders')
    full_name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=255, null=False, blank=False )
    contact_number = models.CharField(max_length=20, null=False, blank=False)

    address_line_1 = models.CharField(max_length=80)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    town_or_city = models.CharField(max_length=40)
    post_code = models.CharField(max_length=20, null=False, blank=False)
    county = models.CharField(max_length=40, null =True , blank =True)
    country = CountryField(blank_label='Country *', max_length=40, null =True , blank =True)
    
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=False)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=False)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2,default=0, null=False)

    date = models.DateTimeField(auto_now_add=True)

    def _generate_order_number(self):
        """ Generate a random order number using UUID """
        return uuid.uuid4().hex.upper()
    
    def update_total(self):
        """ Update grand total & delivery costs each time an item is added  """
        self.subtotal = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.subtotal < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = settings.STANDARD_DELIVERY
        else:
            self.delivery_cost = 0 
        self.grand_total = self.subtotal + self.delivery_cost
        self.save()
    
    def save(self, *args, **kwargs):
        """ Overwrite default save and generate number if not already  """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, blank=False, null=False , on_delete=models.CASCADE, related_name= 'lineitems')
    product = models.ForeignKey(Product, blank=False, null=False , on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False, null=False, default=0 )
    lineitem_total = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    
    def save(self, *args, **kwargs):
        """ Overwrite default save and generate number if not already  """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.order_number})"