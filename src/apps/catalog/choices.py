from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _


class ProductBadgeChoice(models.TextChoices):
    NONE = "", ""
    NEW = "new", _(T.badge_new)
    BESTSELLER = "bestseller", _(T.badge_bestseller)


class WeightUnitChoice(models.TextChoices):
    GRAM = "g", _(T.gram)
    KILOGRAM = "kg", _(T.kilogram)
