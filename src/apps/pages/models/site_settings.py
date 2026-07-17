from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel
from apps.common.utils.phone_validator import phone_validator


class SiteSettings(BaseModel):
    phone = models.CharField(
        max_length=20, blank=True, default="", validators=[phone_validator], verbose_name=_(T.phone)
    )
    hotline = models.CharField(
        max_length=20, blank=True, default="", validators=[phone_validator], verbose_name=_(T.hotline)
    )
    email = models.EmailField(blank=True, default="", verbose_name=_(T.email))
    address = models.JSONField(default=dict, blank=True, verbose_name=_(T.address))
    work_hours = models.JSONField(default=dict, blank=True, verbose_name=_(T.work_hours))
    yandex_map_url = models.URLField(blank=True, verbose_name=_(T.yandex_map_url))
    instagram_url = models.URLField(blank=True, verbose_name=_(T.instagram_url))
    telegram_url = models.URLField(blank=True, verbose_name=_(T.telegram_url))
    catalog_file = models.CharField(max_length=500, blank=True, verbose_name=_(T.catalog_file))
    cookie_notice_text = models.JSONField(default=dict, blank=True, verbose_name=_(T.cookie_notice_text))

    class Meta:
        verbose_name = _(T.site_settings)
        verbose_name_plural = _(T.site_settings)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls) -> "SiteSettings":
        instance, _created = cls.objects.get_or_create(pk=1)
        return instance

    def __str__(self):
        return "Site settings"
