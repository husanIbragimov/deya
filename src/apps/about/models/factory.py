from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel


class Factory(BaseModel):
    title = models.JSONField(default=dict, verbose_name=_(T.title))
    subtitle = models.JSONField(default=dict, blank=True, verbose_name=_(T.subtitle))
    description = models.JSONField(default=dict, blank=True, verbose_name=_(T.description))
    subdescription = models.JSONField(default=dict, blank=True, verbose_name=_(T.subdescription))
    image = models.CharField(max_length=500, verbose_name=_(T.image))

    class Meta:
        verbose_name = _(T.factory)
        verbose_name_plural = _(T.factory)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls) -> "Factory":
        instance, _created = cls.objects.get_or_create(pk=1)
        return instance

    def __str__(self):
        return "Factory"
