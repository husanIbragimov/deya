from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel


class PrivacyPolicy(BaseModel):
    title = models.JSONField(default=dict, verbose_name=_(T.title))
    body = models.JSONField(default=dict, blank=True, verbose_name=_(T.body))

    class Meta:
        verbose_name = _(T.privacy_policy)
        verbose_name_plural = _(T.privacy_policy)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls) -> "PrivacyPolicy":
        instance, _created = cls.objects.get_or_create(pk=1)
        return instance

    def __str__(self):
        return "Privacy policy"
