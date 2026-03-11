from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.text import slugify
from django.views.decorators.http import require_GET, require_POST

from .choices import AssemblyType, FuelType, ProductCondition, ProductStatus, TransmissionType
from .constants import PRODUCTS_PER_PAGE
from .forms import ProductForm
from .models import CarModel, Category, Make, Product, Variant
from .utils import make_unique_slug


@require_GET
def product_list_view(request):
    """
    List active products with search, filters, sorting, and pagination.
    """
    products = Product.objects.all()

    # Search across product and related make/model/variant fields.
    query = request.GET.get("q")
    if query:
        products = products.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(make__name__icontains=query)
            | Q(model__name__icontains=query)
            | Q(variant__name__icontains=query)
            | Q(registered_city__icontains=query)
            | Q(color__icontains=query)
            | Q(ad_reference_id__icontains=query)
        )

    # Basic filters
    category_slug = request.GET.get("category")
    if category_slug:
        products = products.filter(category__slug=category_slug)

    make_slug = request.GET.get("make")
    if make_slug:
        products = products.filter(make__slug=make_slug)

    model_slug = request.GET.get("model")
    if model_slug:
        products = products.filter(model__slug=model_slug)

    variant_slug = request.GET.get("variant")
    if variant_slug:
        products = products.filter(variant__slug=variant_slug)

    status = request.GET.get("status")
    if status:
        products = products.filter(status=status)

    condition = request.GET.get("condition")
    if condition:
        products = products.filter(condition=condition)

    fuel_type = request.GET.get("fuel_type")
    if fuel_type:
        products = products.filter(fuel_type=fuel_type)

    transmission = request.GET.get("transmission")
    if transmission:
        products = products.filter(transmission=transmission)

    assembly_type = request.GET.get("assembly_type")
    if assembly_type:
        products = products.filter(assembly_type=assembly_type)

    # Range filters
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    min_year = request.GET.get("min_year")
    max_year = request.GET.get("max_year")
    if min_year:
        products = products.filter(year__gte=min_year)
    if max_year:
        products = products.filter(year__lte=max_year)

    min_mileage = request.GET.get("min_mileage")
    max_mileage = request.GET.get("max_mileage")
    if min_mileage:
        products = products.filter(mileage__gte=min_mileage)
    if max_mileage:
        products = products.filter(mileage__lte=max_mileage)

    min_engine_cc = request.GET.get("min_engine_cc")
    max_engine_cc = request.GET.get("max_engine_cc")
    if min_engine_cc:
        products = products.filter(engine_capacity_cc__gte=min_engine_cc)
    if max_engine_cc:
        products = products.filter(engine_capacity_cc__lte=max_engine_cc)

    # Additional text filters
    registered_city = request.GET.get("registered_city")
    if registered_city:
        products = products.filter(registered_city__icontains=registered_city)

    body_type = request.GET.get("body_type")
    if body_type:
        products = products.filter(body_type__icontains=body_type)

    color = request.GET.get("color")
    if color:
        products = products.filter(color__icontains=color)

    # Sorting
    sort = request.GET.get("sort")
    if sort == "oldest":
        products = products.order_by("created")
    elif sort == "newest":
        products = products.order_by("-created")
    elif sort == "price_asc":
        products = products.order_by("price", "-created")
    elif sort == "price_desc":
        products = products.order_by("-price", "-created")
    elif sort == "year_asc":
        products = products.order_by("year", "-created")
    elif sort == "year_desc":
        products = products.order_by("-year", "-created")
    elif sort == "mileage_asc":
        products = products.order_by("mileage", "-created")
    elif sort == "mileage_desc":
        products = products.order_by("-mileage", "-created")
    else:
        # Default uses TimeStampedModel.created.
        products = products.order_by("-created")

    paginator = Paginator(products, PRODUCTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    makes = Make.objects.all()
    models = CarModel.objects.select_related("make").all()
    variants = Variant.objects.select_related("model", "model__make").all()

    context = {
        "page_obj": page_obj,
        "categories": categories,
        "makes": makes,
        "models": models,
        "variants": variants,
        "condition_choices": ProductCondition.choices,
        "status_choices": ProductStatus.choices,
        "fuel_type_choices": FuelType.choices,
        "transmission_choices": TransmissionType.choices,
        "assembly_type_choices": AssemblyType.choices,
    }
    return render(request, "store/product_list.html", context)


@login_required
@require_POST
def product_add_view(request):
    """
    Create a new product. Seller is set to request.user.
    Slug is generated from title and made unique.
    """
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            base_slug = slugify(product.title) or "product"
            product.slug = make_unique_slug(base_slug, Product)
            product.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "store/product_form.html", {"form": form})
