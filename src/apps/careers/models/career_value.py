from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel
from apps.common.utils.translated_value import translated_value


class CareerValue(BaseModel):
    title = models.JSONField(default=dict, verbose_name=_(T.title))
    text = models.JSONField(default=dict, verbose_name=_(T.text))
    image = models.CharField(max_length=500, blank=True, verbose_name=_(T.image))

    class Meta:
        ordering = ("id",)
        verbose_name = _(T.career_value)
        verbose_name_plural = _(T.career_values)

    def __str__(self):
        return translated_value(self.title)
