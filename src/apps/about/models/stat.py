from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel
from apps.common.utils.translated_value import translated_value


class Stat(BaseModel):
    value = models.CharField(max_length=16, verbose_name=_(T.weight_value))
    label = models.JSONField(default=dict, verbose_name=_(T.label))

    class Meta:
        ordering = ("id",)
        verbose_name = _(T.stat)
        verbose_name_plural = _(T.stats)

    def __str__(self):
        return f"{self.value} {translated_value(self.label)}"
