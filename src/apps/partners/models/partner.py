from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel


class Partner(BaseModel):
    name = models.CharField(max_length=150, verbose_name=_(T.common_name))
    logo = models.CharField(max_length=500, verbose_name=_(T.logo))
    website = models.URLField(blank=True, verbose_name=_(T.website))

    class Meta:
        ordering = ("name",)
        verbose_name = _(T.partner)
        verbose_name_plural = _(T.partners)

    def __str__(self):
        return self.name
