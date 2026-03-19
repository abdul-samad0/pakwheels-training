from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.views.decorators.http import require_GET, require_POST

from .choices import AssemblyType, FuelType, ProductCondition, ProductStatus, TransmissionType
from .constants import PRODUCTS_PER_PAGE
from .forms import CategoryForm, ProductForm
from .models import CarModel, Category, Favorite, Like, Product, Rating
from .utils import make_unique_slug


@login_required
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
            | Q(model__name__icontains=query)
            | Q(model__make__icontains=query)
            | Q(model__variant__icontains=query)
            | Q(registered_city__icontains=query)
            | Q(color__icontains=query)
            | Q(ad_reference_id__icontains=query)
        )

    # Basic filters
    category_slug = request.GET.get("category")
    if category_slug:
        products = products.filter(category__slug=category_slug)

    make_name = request.GET.get("make")
    if make_name:
        products = products.filter(model__make=make_name)

    model_slug = request.GET.get("model")
    if model_slug:
        products = products.filter(model__slug=model_slug)

    variant_name = request.GET.get("variant")
    if variant_name:
        products = products.filter(model__variant=variant_name)

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
    makes = CarModel.objects.values_list(
        "make", flat=True).distinct().order_by("make")
    models = CarModel.objects.all()
    variants = CarModel.objects.exclude(variant="").values_list(
        "variant", flat=True).distinct().order_by("variant")
    favorite_product_ids = list(
        Favorite.objects.filter(
            user=request.user,
            product_id__in=[item.id for item in page_obj.object_list],
        ).values_list("product_id", flat=True)
    )
    like_product_ids = list(
        Like.objects.filter(
            user=request.user,
            product_id__in=[item.id for item in page_obj.object_list],
        ).values_list("product_id", flat=True)
    )
    get_dict = request.GET.copy()
    if "page" in get_dict:
        get_dict.pop("page")
    query_string = get_dict.urlencode()

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
        "query_string": query_string,
        "favorite_product_ids": favorite_product_ids,
        "like_product_ids": like_product_ids,
    }
    return render(request, "store/product_list.html", context)


@login_required
def product_add_view(request):
    """
    Create a new product. Seller is set to request.user.
    Slug is generated from title and made unique.
    """
    has_categories = Category.objects.exists()

    if request.method == "POST":
        form = ProductForm(request.POST)
        if not has_categories:
            form.add_error(
                "category", "No categories exist. Please create a category first.")
        elif form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            base_slug = slugify(product.title) or "product"
            product.slug = make_unique_slug(base_slug, Product)
            product.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(
        request,
        "store/product_form.html",
        {
            "form": form,
            "has_categories": has_categories,
        },
    )


@login_required
def category_add_view(request):
    """Create a category so products can reference it."""
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            base_slug = slugify(category.name) or "category"
            category.slug = make_unique_slug(base_slug, Category)
            category.save()
            return redirect("product_add")
    else:
        form = CategoryForm()
    return render(request, "store/category_form.html", {"form": form})


@login_required
@require_GET
def product_detail_view(request, slug):
    """Render one product with full details and images."""
    product = get_object_or_404(
        Product.objects.filter(
            slug=slug,
            is_active=True,
        ))
    is_favorite = Favorite.objects.filter(
        user=request.user, product=product).exists()
    is_liked = Like.objects.filter(user=request.user, product=product).exists()
    user_rating = Rating.objects.filter(user=request.user, product=product).first()
    rating_summary = Rating.objects.filter(product=product).aggregate(
        average_rating=Avg("score")
    )
    return render(
        request,
        "store/product_detail.html",
        {
            "product": product,
            "is_favorite": is_favorite,
            "is_liked": is_liked,
            "like_count": Like.objects.filter(product=product).count(),
            "user_rating": user_rating.score if user_rating else None,
            "average_rating": rating_summary["average_rating"],
            "rating_count": Rating.objects.filter(product=product).count(),
        },
    )


@login_required
@require_POST
def favorite_toggle_view(request, slug):
    """Toggle favorite state and return the current state."""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    is_favorite = Favorite.objects.filter(
        user=request.user, product=product).exists()

    if is_favorite:
        Favorite.objects.filter(user=request.user, product=product).delete()
        is_favorite = False
    else:
        Favorite.objects.get_or_create(user=request.user, product=product)
        is_favorite = True

    return JsonResponse({"is_favorite": is_favorite, "product_id": product.id})


@login_required
@require_POST
def like_toggle_view(request, slug):
    """Toggle like state and return the current state."""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    is_liked = Like.objects.filter(user=request.user, product=product).exists()

    if is_liked:
        Like.objects.filter(user=request.user, product=product).delete()
        is_liked = False
    else:
        Like.objects.get_or_create(user=request.user, product=product)
        is_liked = True

    like_count = Like.objects.filter(product=product).count()
    return JsonResponse(
        {"is_liked": is_liked, "like_count": like_count, "product_id": product.id}
    )


@login_required
@require_POST
def product_rating_view(request, slug):
    """Create or update rating for a product."""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    raw_score = request.POST.get("score")

    try:
        score = int(raw_score)
    except (TypeError, ValueError):
        return JsonResponse({"error": "Invalid rating value."}, status=400)

    if score < 1 or score > 5:
        return JsonResponse({"error": "Rating must be between 1 and 5."}, status=400)

    Rating.objects.update_or_create(
        user=request.user,
        product=product,
        defaults={"score": score},
    )
    summary = Rating.objects.filter(product=product).aggregate(average_rating=Avg("score"))
    rating_count = Rating.objects.filter(product=product).count()

    return JsonResponse(
        {
            "score": score,
            "average_rating": summary["average_rating"],
            "rating_count": rating_count,
            "product_id": product.id,
        }
    )


@login_required
@require_GET
def favorite_list_view(request):
    """Render the authenticated user's favorite products."""
    favorites = Favorite.objects.filter(
        user=request.user, product__is_active=True).order_by("-created")
    return render(request, "store/favorite_list.html", {"favorites": favorites})
