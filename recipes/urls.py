from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipes'),
    path('<recipe_id>/', views.recipe_details, name='recipe_details'),
]