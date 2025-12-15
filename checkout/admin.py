from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = (
        'order_number',
        'date',
        'delivery_cost',
        'subtotal',
        'grand_total',
    )

    fields = (
        'order_number',
        'date',
        'full_name',
        'email',
        'contact_number',
        'town_or_city',
        'address_line_1',
        'address_line_2',
        'post_code',
        'county',
        'country',
        'delivery_cost',
        'subtotal',
        'grand_total',
    )

    list_display = (
        'order_number',
        'date',
        'full_name',
        'subtotal',
        'grand_total',
    )

    ordering = ('-date',)  # Most recent orders first


admin.site.register(Order, OrderAdmin)
