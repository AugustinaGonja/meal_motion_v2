from django import forms
from .models import Order

# Django Form Customisation

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name','email','contact_number',
                'town_or_city','address_line_1',
                'address_line_2','post_code','county',
                'country',)
        
    def __init__(self, *args , **kwargs ):
        """Remove and replace labels with Placeholders """
        super().__init__(*args , **kwargs)
        placeholders = {
            'full_name' : 'Full Name',
            'email': 'Email',
            'contact_number': 'Contact Number',
            'town_or_city': 'Town or City',
            'address_line_1': 'Address Line 1',
            'address_line_2': 'Address Line 2',
            'post_code': 'Post Code',
            'county': 'County',
            'country':'Country',
        }
        
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]

            self.fields[field].widget.attrs.update({
                'placeholder': placeholder,
                'class': 'form-control mb-3'
            })
            self.fields[field].label = False