from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel
from apps.common.utils.translated_value import translated_value


class StaticPage(BaseModel):
    slug = models.SlugField(max_length=170, unique=True, db_index=True, verbose_name=_(T.slug))
    title = models.JSONField(default=dict, verbose_name=_(T.title))
    body = models.JSONField(default=dict, blank=True, verbose_name=_(T.body))

    class Meta:
        ordering = ("slug",)
        verbose_name = _(T.static_page)
        verbose_name_plural = _(T.static_pages)

    def __str__(self):
        return translated_value(self.title)
