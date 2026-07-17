from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel
from apps.common.utils.translated_value import translated_value


class HomeSlide(BaseModel):
    title = models.JSONField(default=dict, verbose_name=_(T.title))
    subtitle = models.JSONField(default=dict, blank=True, verbose_name=_(T.subtitle))
    image = models.CharField(max_length=500, verbose_name=_(T.image))
    cta_label = models.JSONField(default=dict, blank=True, verbose_name=_(T.cta_label))
    cta_url = models.URLField(blank=True, verbose_name=_(T.cta_url))

    class Meta:
        ordering = ("id",)
        verbose_name = _(T.home_slide)
        verbose_name_plural = _(T.home_slides)

    def __str__(self):
        return translated_value(self.title)
