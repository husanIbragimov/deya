from django.db import models

from apps.catalog.models.product import Product
from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name=_(T.product))
    image = models.CharField(max_length=500, verbose_name=_(T.image))
    alt = models.JSONField(default=dict, blank=True, verbose_name=_(T.alt))
    is_main = models.BooleanField(default=False, verbose_name=_(T.is_main))
    sort_order = models.PositiveSmallIntegerField(default=0, db_index=True, verbose_name=_(T.sort_order))

    class Meta:
        ordering = ("sort_order", "id")
        verbose_name = _(T.product_image)
        verbose_name_plural = _(T.product_images)

    def __str__(self):
        return f"{self.product_id}:{self.pk}"
