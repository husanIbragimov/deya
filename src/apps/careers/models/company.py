from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel


class Company(BaseModel):
    name = models.CharField(max_length=150, verbose_name=_(T.common_name))
    slug = models.SlugField(max_length=170, unique=True, db_index=True, verbose_name=_(T.slug))
    description = models.JSONField(default=dict, blank=True, verbose_name=_(T.description))
    image = models.CharField(max_length=500, verbose_name=_(T.image))
    vacancies_url = models.URLField(blank=True, verbose_name=_(T.vacancies_url))

    class Meta:
        ordering = ("name",)
        verbose_name = _(T.company)
        verbose_name_plural = _(T.companies)

    def __str__(self):
        return self.name
