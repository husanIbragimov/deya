from django.db import models

from apps.catalog.choices import BoxQuantityUnitChoice
from apps.common.choices import choices_help_text
from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _


class BoxQuantityMixin(models.Model):
    """ "Quantity per box" (kg/pcs).

    Set on `ProductFamily` as the shared value for all variants, and on `Product` to override it per variant.
    Quantity and unit are either both set or both empty.
    """

    box_quantity = models.DecimalField(
        max_digits=10, decimal_places=3, null=True, blank=True, verbose_name=_(T.box_quantity)
    )
    box_quantity_unit = models.CharField(
        max_length=3,
        choices=BoxQuantityUnitChoice.choices,
        blank=True,
        default="",
        verbose_name=_(T.box_quantity_unit),
        help_text=choices_help_text(BoxQuantityUnitChoice),
    )

    class Meta:
        abstract = True


def box_quantity_constraint(name: str) -> models.CheckConstraint:
    return models.CheckConstraint(
        condition=(
            models.Q(box_quantity__isnull=True, box_quantity_unit="")
            | (models.Q(box_quantity__isnull=False) & ~models.Q(box_quantity_unit=""))
        ),
        name=name,
    )
