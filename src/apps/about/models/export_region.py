from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel
from apps.common.utils.translated_value import translated_value


class ExportRegion(BaseModel):
    name = models.JSONField(default=dict, verbose_name=_(T.common_name))
    position_x = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_(T.position_x))
    position_y = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_(T.position_y))

    class Meta:
        ordering = ("id",)
        verbose_name = _(T.export_region)
        verbose_name_plural = _(T.export_regions)

    def __str__(self):
        return translated_value(self.name)
