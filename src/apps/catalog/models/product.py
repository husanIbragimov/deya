from django.db import models

from apps.catalog.choices import ProductBadgeChoice
from apps.catalog.models.box_quantity import BoxQuantityMixin, box_quantity_constraint
from apps.catalog.models.category import Category
from apps.catalog.models.flavor import Flavor
from apps.catalog.models.product_family import ProductFamily
from apps.catalog.models.weight import Weight
from apps.common.choices import choices_help_text
from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel
from apps.common.utils.translated_value import translated_value


class Product(BoxQuantityMixin, BaseModel):
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
    weight = models.ForeignKey(
        Weight, on_delete=models.SET_NULL, null=True, blank=True, related_name="products", verbose_name=_(T.weight)
    )
    badge = models.CharField(
        max_length=16,
        choices=ProductBadgeChoice.choices,
        blank=True,
        default=ProductBadgeChoice.NONE,
        verbose_name=_(T.badge),
        help_text=choices_help_text(ProductBadgeChoice),
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
        constraints = [
            models.UniqueConstraint(
                fields=("family", "flavor", "weight"),
                condition=models.Q(family__isnull=False),
                name="unique_product_family_flavor_weight",
            ),
            box_quantity_constraint("product_box_quantity_with_unit"),
        ]
        indexes = [
            models.Index(fields=("category", "is_active", "sort_order")),
            models.Index(fields=("badge",)),
            models.Index(fields=("is_featured",)),
        ]

    def _box_quantity_source(self):
        """Variant's own quantity per box wins; otherwise the family's shared value is used."""
        if self.box_quantity is None and self.family is not None and self.family.box_quantity is not None:
            return self.family
        return self

    @property
    def effective_box_quantity(self):
        return self._box_quantity_source().box_quantity

    @property
    def effective_box_quantity_unit(self) -> str:
        return self._box_quantity_source().box_quantity_unit

    def __str__(self):
        return f"{self.code} — {translated_value(self.name)}"
