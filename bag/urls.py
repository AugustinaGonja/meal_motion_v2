from django.urls import path
from . import views

urlpatterns = [
    path('', views.shopping_bag, name='bag'),
     path('add/<int:item_id>', views.add_items, name='add_items'),
]
