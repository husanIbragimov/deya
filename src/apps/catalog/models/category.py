from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel
from apps.common.utils.translated_value import translated_value


class Category(BaseModel):
    name = models.JSONField(default=dict, verbose_name=_(T.common_name))
    slug = models.SlugField(max_length=170, unique=True, db_index=True, verbose_name=_(T.slug))
    image = models.CharField(max_length=500, verbose_name=_(T.image))
    sort_order = models.PositiveSmallIntegerField(default=0, db_index=True, verbose_name=_(T.sort_order))
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_(T.active))

    class Meta:
        ordering = ("sort_order", "id")
        verbose_name = _(T.category)
        verbose_name_plural = _(T.categories)

    def __str__(self):
        return translated_value(self.name)
