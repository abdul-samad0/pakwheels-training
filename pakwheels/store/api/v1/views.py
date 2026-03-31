from django.db.models import Q
from rest_framework import generics

from pakwheels.store.models import Category, Product

from .serializers import (
    CategorySerializer,
    ProductCreateSerializer,
    ProductListSerializer,
)


class CategoryCreateAPIView(generics.CreateAPIView):
    serializer_class = CategorySerializer

class ProductListCreateAPIView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductCreateSerializer
        return ProductListSerializer

    def get_queryset(self):
        products = Product.objects.all()

        query = self.request.query_params.get("q")
        if query:
            products = products.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(model__name__icontains=query)
                | Q(model__make__icontains=query)
                | Q(model__variant__icontains=query)
                | Q(registered_city__icontains=query)
                | Q(color__icontains=query)
                | Q(ad_reference_id__icontains=query)
            )

        category_slug = self.request.query_params.get("category")
        if category_slug:
            products = products.filter(category__slug=category_slug)

        make_name = self.request.query_params.get("make")
        if make_name:
            products = products.filter(model__make=make_name)

        model_slug = self.request.query_params.get("model")
        if model_slug:
            products = products.filter(model__slug=model_slug)

        variant_name = self.request.query_params.get("variant")
        if variant_name:
            products = products.filter(model__variant=variant_name)

        status = self.request.query_params.get("status")
        if status:
            products = products.filter(status=status)

        condition = self.request.query_params.get("condition")
        if condition:
            products = products.filter(condition=condition)

        fuel_type = self.request.query_params.get("fuel_type")
        if fuel_type:
            products = products.filter(fuel_type=fuel_type)

        transmission = self.request.query_params.get("transmission")
        if transmission:
            products = products.filter(transmission=transmission)

        assembly_type = self.request.query_params.get("assembly_type")
        if assembly_type:
            products = products.filter(assembly_type=assembly_type)

        registered_city = self.request.query_params.get("registered_city")
        if registered_city:
            products = products.filter(
                registered_city__icontains=registered_city)

        body_type = self.request.query_params.get("body_type")
        if body_type:
            products = products.filter(body_type__icontains=body_type)

        color = self.request.query_params.get("color")
        if color:
            products = products.filter(color__icontains=color)

        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        min_year = self.request.query_params.get("min_year")
        max_year = self.request.query_params.get("max_year")
        if min_year:
            products = products.filter(year__gte=min_year)
        if max_year:
            products = products.filter(year__lte=max_year)

        min_mileage = self.request.query_params.get("min_mileage")
        max_mileage = self.request.query_params.get("max_mileage")
        if min_mileage:
            products = products.filter(mileage__gte=min_mileage)
        if max_mileage:
            products = products.filter(mileage__lte=max_mileage)

        min_engine_cc = self.request.query_params.get("min_engine_cc")
        max_engine_cc = self.request.query_params.get("max_engine_cc")
        if min_engine_cc:
            products = products.filter(engine_capacity_cc__gte=min_engine_cc)
        if max_engine_cc:
            products = products.filter(engine_capacity_cc__lte=max_engine_cc)

        sort = self.request.query_params.get("sort")
        if sort == "oldest":
            return products.order_by("created")
        if sort == "price_asc":
            return products.order_by("price", "-created")
        if sort == "price_desc":
            return products.order_by("-price", "-created")
        if sort == "year_asc":
            return products.order_by("year", "-created")
        if sort == "year_desc":
            return products.order_by("-year", "-created")
        if sort == "mileage_asc":
            return products.order_by("mileage", "-created")
        if sort == "mileage_desc":
            return products.order_by("-mileage", "-created")

        return products.order_by("-created")
