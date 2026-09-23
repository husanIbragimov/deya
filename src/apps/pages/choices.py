from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _


class BannerTypeChoice(models.TextChoices):
    MAIN = "main", _(T.banner_main)
    ABOUT = "about", _(T.banner_about)
    CARRIER = "carrier", _(T.banner_carrier)
    PARTNER = "partner", _(T.banner_partner)
    SUB_MAIN = "sub_main", _(T.sub_main)
    SUB_MAIN_MAP = "sub_main_map", _(T.sub_main_map)
    ABOUT_TITLE = "about_title", _(T.about_title)
