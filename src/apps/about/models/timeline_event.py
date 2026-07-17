from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel
from apps.common.utils.translated_value import translated_value


class TimelineEvent(BaseModel):
    year = models.PositiveSmallIntegerField(unique=True, db_index=True, verbose_name=_(T.year))
    title = models.JSONField(default=dict, verbose_name=_(T.title))
    description = models.JSONField(default=dict, blank=True, verbose_name=_(T.description))
    image = models.CharField(max_length=500, blank=True, verbose_name=_(T.image))

    class Meta:
        ordering = ("year",)
        verbose_name = _(T.timeline_event)
        verbose_name_plural = _(T.timeline_events)

    def __str__(self):
        return f"{self.year} — {translated_value(self.title)}"
