from django import forms
from .models import UserProfile

# Django Form Customization


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """Remove labels and replace them with placeholders."""
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_contact_number': 'Contact Number',
            'default_town_or_city': 'Town or City',
            'default_address_line_1': 'Address Line 1',
            'default_address_line_2': 'Address Line 2',
            'default_post_code': 'Post Code',
            'default_county': 'County',
            'default_country': 'Country',
        }

        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]

            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False
