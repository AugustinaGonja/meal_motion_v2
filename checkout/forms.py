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

        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (
                f"{existing_classes} form-control mb-3".strip()
            )

            label = placeholders[field_name]
            suffix = " *" if field.required else ""
            text = f"{label}{suffix}"

        if isinstance(field, forms.ChoiceField):
            field.choices = [("", text), *field.choices]
        else:
            field.widget.attrs["placeholder"] = text

        field.label = False
