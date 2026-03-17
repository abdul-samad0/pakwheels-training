from django import forms

from .models import CarModel, Category, Product


class ProductForm(forms.ModelForm):
    """Form for creating a product. Slug is generated from title in the view."""

    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "price",
            "location",
            "condition",
            "category",
            "model",
            "status",
            "fuel_type",
            "transmission",
            "assembly_type",
            "year",
            "mileage",
            "engine_capacity_cc",
            "registered_city",
            "body_type",
            "color",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "model": forms.Select(attrs={"class": "form-select"}),
            "year": forms.NumberInput(attrs={"min": 1900, "max": 2100, "placeholder": "e.g. 2020"}),
            "mileage": forms.NumberInput(attrs={"min": 0, "placeholder": "km"}),
            "engine_capacity_cc": forms.NumberInput(attrs={"min": 0, "placeholder": "cc"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.order_by("name")
        self.fields["category"].empty_label = "Select category"
        self.fields["model"].queryset = CarModel.objects.order_by(
            "make", "name", "variant")
        self.fields["model"].required = False
        self.fields["model"].empty_label = "Select make/model (optional)"
        self.fields["status"].required = True
        self.fields["fuel_type"].required = False
        self.fields["transmission"].required = False
        self.fields["assembly_type"].required = False
        self.fields["year"].required = False
        self.fields["mileage"].required = False
        self.fields["engine_capacity_cc"].required = False
        self.fields["registered_city"].required = False
        self.fields["body_type"].required = False
        self.fields["color"].required = False


class CategoryForm(forms.ModelForm):
    """Form for creating a category. Slug is generated from name in the view."""

    class Meta:
        model = Category
        fields = ["name", "parent"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["parent"].queryset = Category.objects.order_by("name")
        if self.instance and self.instance.pk:
            self.fields["parent"].queryset = self.fields["parent"].queryset.exclude(
                pk=self.instance.pk)
        self.fields["parent"].empty_label = "No parent (top-level)"
