def make_unique_slug(base_slug, model_class):
    """Generate a unique slug; append -1, -2, ... if base_slug is taken."""
    slug = base_slug
    counter = 1
    while model_class.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug

