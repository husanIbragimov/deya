from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _


class BannerTypeChoice(models.TextChoices):
    PARTNER = "partner", _(T.banner_type_partner)
