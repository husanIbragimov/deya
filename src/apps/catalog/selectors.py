from django.db.models import QuerySet

from apps.catalog.models import Category, Product


def active_categories() -> QuerySet[Category]:
    return Category.objects.filter(is_active=True).order_by("sort_order", "id")


def product_base_queryset() -> QuerySet[Product]:
    return (
        Product.objects.filter(is_active=True)
        .select_related("category", "family", "flavor")
        .prefetch_related("images", "weights")
    )


def get_product_by_slug(slug: str) -> Product:
    return product_base_queryset().get(slug=slug)


def featured_products(limit: int = 4) -> QuerySet[Product]:
    return product_base_queryset().filter(is_featured=True).order_by("sort_order", "id")[:limit]


def get_family_variants(product: Product) -> QuerySet[Product]:
    if not product.family_id:
        return Product.objects.none()
    return product_base_queryset().filter(family_id=product.family_id).exclude(pk=product.pk)


def get_related_products(product: Product) -> QuerySet[Product]:
    related = (
        product.related_products.filter(is_active=True)
        .select_related("category", "family", "flavor")
        .prefetch_related("images", "weights")
    )
    if related.exists():
        return related
    return product_base_queryset().filter(category_id=product.category_id).exclude(pk=product.pk)
