from django import forms
from .models import Order

# Django Form Customisation


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name',
            'email',
            'contact_number',
            'town_or_city',
            'address_line_1',
            'address_line_2',
            'post_code',
            'county',
            'country',
            )

    def __init__(self, *args, **kwargs):
        """Remove and replace labels with Placeholders """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email',
            'contact_number': 'Contact Number',
            'town_or_city': 'Town or City',
            'address_line_1': 'Address Line 1',
            'address_line_2': 'Address Line 2',
            'post_code': 'Postcode',
            'county': 'County',
            'country': 'Country',
        }

        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing_classes} form-control mb-3'.strip()

            if isinstance(field, forms.ChoiceField):
                empty_label = f"{placeholders[field_name]} *" if field.required else placeholders[field_name]
                field.choices = [('', empty_label)] + list(field.choices)
            else:
                placeholder = f"{placeholders[field_name]} *" if field.required else placeholders[field_name]
                field.widget.attrs['placeholder'] = placeholder

            field.label = False
