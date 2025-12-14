from django.contrib import admin
from .models import Product, Category

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'price')
    search_fields = ('name', 'description', 'category__name')
    list_filter = ('category',)
    ordering = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name')
    search_fields = ('name',)


admin.site.register(Product)
admin.site.register(Category)
