from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel
from apps.common.utils.translated_value import translated_value


class Post(BaseModel):
    title = models.JSONField(default=dict, verbose_name=_(T.title))
    slug = models.SlugField(max_length=220, unique=True, db_index=True, verbose_name=_(T.slug))
    excerpt = models.JSONField(default=dict, blank=True, verbose_name=_(T.excerpt))
    cover = models.CharField(max_length=500, verbose_name=_(T.cover))
    published_at = models.DateTimeField(db_index=True, verbose_name=_(T.published_at))
    is_published = models.BooleanField(default=True, verbose_name=_(T.is_published))

    class Meta:
        ordering = ("-published_at",)
        verbose_name = _(T.post)
        verbose_name_plural = _(T.posts)
        indexes = [
            models.Index(fields=("is_published", "-published_at")),
        ]

    def __str__(self):
        return translated_value(self.title)
