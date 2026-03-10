from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.text import slugify

from .models import Product, Category
from .forms import ProductForm


def product_list_view(request):
    """
    List active products with search, category/price/condition filters,
    sorting, and pagination. Uses select_related for seller/category.
    """
    products =Product.objects.all()

    # Search (Q: title OR description)
    query = request.GET.get("q")
    if query:
        products = products.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # Category filter (double-underscore lookup)
    category_slug = request.GET.get("category")
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Price filters
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Condition filter
    condition = request.GET.get("condition")
    if condition:
        products = products.filter(condition=condition)

    # Sorting (default: newest first via TimeStampedModel.created)
    sort = request.GET.get("sort")
    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    else:
        products = products.order_by("-created")

    # Pagination (triggers query execution)
    paginator = Paginator(products, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()


    context = {
        "page_obj": page_obj,
        "categories": categories,
    }
    return render(request, "store/product_list.html", context)


def _make_unique_slug(base_slug, model_class):
    """Generate a unique slug; append -1, -2, ... if base_slug is taken."""
    slug = base_slug
    counter = 1
    while model_class.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


@login_required
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
            product.slug = _make_unique_slug(base_slug, Product)
            product.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "store/product_form.html", {"form": form})
