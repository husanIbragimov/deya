from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel


class ProductFamily(BaseModel):
    name = models.CharField(max_length=150, verbose_name=_(T.common_name))
    slug = models.SlugField(max_length=170, unique=True, db_index=True, verbose_name=_(T.slug))

    class Meta:
        ordering = ("name",)
        verbose_name = _(T.product_family)
        verbose_name_plural = _(T.product_families)

    def __str__(self):
        return self.name
