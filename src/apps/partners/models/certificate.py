from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel
from apps.common.utils.translated_value import translated_value


class Certificate(BaseModel):
    title = models.JSONField(default=dict, verbose_name=_(T.title))
    image = models.CharField(max_length=500, verbose_name=_(T.image))
    file = models.CharField(max_length=500, blank=True, verbose_name=_(T.file))

    class Meta:
        ordering = ("id",)
        verbose_name = _(T.certificate)
        verbose_name_plural = _(T.certificates)

    def __str__(self):
        return translated_value(self.title)
