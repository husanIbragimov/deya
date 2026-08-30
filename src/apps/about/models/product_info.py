from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel
from apps.common.utils.translated_value import translated_value


class ProductInfo(BaseModel):
    title = models.JSONField(default=dict, verbose_name=_(T.title))
    description = models.JSONField(default=dict, blank=True, verbose_name=_(T.description))
    image = models.CharField(max_length=500, verbose_name=_(T.product_image))

    class Meta:
        ordering = ("id",)
        verbose_name = _(T.product_info)
        verbose_name_plural = _(T.product_infos)

    def __str__(self):
        return translated_value(self.title)
