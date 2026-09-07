from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _


class BannerTypeChoice(models.TextChoices):
    MAIN = "main", _(T.banner_main)
    ABOUT = "about", _(T.banner_about)
    CARRIER = "carrier", _(T.banner_carrier)
    PARTNER = "partner", _(T.banner_partner)
