from django.db import models

from apps.catalog.choices import ProductBadgeChoice
from apps.catalog.models.category import Category
from apps.catalog.models.flavor import Flavor
from apps.catalog.models.product_family import ProductFamily
from apps.catalog.models.weight import Weight
from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel
from apps.common.utils.translated_value import translated_value


class Product(BaseModel):
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products", verbose_name=_(T.category)
    )
    family = models.ForeignKey(
        ProductFamily,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name=_(T.product_family),
    )
    flavor = models.ForeignKey(
        Flavor, on_delete=models.SET_NULL, null=True, blank=True, related_name="products", verbose_name=_(T.flavor)
    )
    name = models.JSONField(default=dict, verbose_name=_(T.common_name))
    slug = models.SlugField(max_length=220, unique=True, db_index=True, verbose_name=_(T.slug))
    description = models.JSONField(default=dict, blank=True, verbose_name=_(T.description))
    code = models.CharField(max_length=32, unique=True, verbose_name=_(T.code))
    box_weight = models.DecimalField(max_digits=8, decimal_places=3, verbose_name=_(T.box_weight))
    shelf_life_months = models.PositiveSmallIntegerField(verbose_name=_(T.shelf_life_months))
    weights = models.ManyToManyField(Weight, blank=True, related_name="products", verbose_name=_(T.weights))
    badge = models.CharField(
        max_length=16,
        choices=ProductBadgeChoice.choices,
        blank=True,
        default=ProductBadgeChoice.NONE,
        verbose_name=_(T.badge),
    )
    is_featured = models.BooleanField(default=False, db_index=True, verbose_name=_(T.is_featured))
    related_products = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="recommended_by", verbose_name=_(T.related_products)
    )
    sort_order = models.PositiveSmallIntegerField(default=0, db_index=True, verbose_name=_(T.sort_order))
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_(T.active))

    class Meta:
        ordering = ("sort_order", "id")
        verbose_name = _(T.product)
        verbose_name_plural = _(T.products)
        indexes = [
            models.Index(fields=("category", "is_active", "sort_order")),
            models.Index(fields=("badge",)),
            models.Index(fields=("is_featured",)),
        ]

    def __str__(self):
        return f"{self.code} — {translated_value(self.name)}"
