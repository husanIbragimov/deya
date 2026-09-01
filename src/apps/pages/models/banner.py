from django.db import models

from apps.common.choices import choices_help_text
from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel
from apps.common.utils.translated_value import translated_value
from apps.pages.choices import BannerTypeChoice


class Banner(BaseModel):
    type = models.CharField(
        max_length=16,
        choices=BannerTypeChoice.choices,
        db_index=True,
        verbose_name=_(T.banner_type),
        help_text=choices_help_text(BannerTypeChoice),
    )
    title = models.JSONField(default=dict, verbose_name=_(T.title))
    subtitle = models.JSONField(default=dict, blank=True, verbose_name=_(T.subtitle))
    image = models.CharField(max_length=500, verbose_name=_(T.image))
    cta_label = models.JSONField(default=dict, blank=True, verbose_name=_(T.cta_label))
    cta_url = models.URLField(blank=True, verbose_name=_(T.cta_url))

    class Meta:
        ordering = ("id",)
        verbose_name = _(T.banner)
        verbose_name_plural = _(T.banners)
        indexes = [
            models.Index(fields=("type", "id")),
        ]

    def __str__(self):
        return f"{self.get_type_display()}: {translated_value(self.title)}"
