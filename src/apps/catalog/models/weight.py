from django.db import models

from apps.catalog.choices import WeightUnitChoice
from apps.common.choices import choices_help_text
from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel


class Weight(BaseModel):
    value = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_(T.weight_value))
    unit = models.CharField(
        max_length=2,
        choices=WeightUnitChoice.choices,
        verbose_name=_(T.unit),
        help_text=choices_help_text(WeightUnitChoice),
    )

    class Meta:
        ordering = ("unit", "value")
        constraints = [
            models.UniqueConstraint(fields=("value", "unit"), name="unique_weight_value_unit"),
        ]
        verbose_name = _(T.weight)
        verbose_name_plural = _(T.weights)

    def __str__(self):
        return f"{self.value} {self.unit}"
