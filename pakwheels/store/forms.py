from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    """Form for creating a product. Slug is generated from title in the view."""

    class Meta:
        model = Product
        fields = ["title", "description", "price", "location", "condition", "category"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }
