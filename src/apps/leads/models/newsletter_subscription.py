import uuid

from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel


class NewsletterSubscription(BaseModel):
    email = models.EmailField(unique=True, db_index=True, verbose_name=_(T.email))
    is_active = models.BooleanField(default=True, verbose_name=_(T.active))
    unsubscribe_token = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, verbose_name=_(T.unsubscribe_token)
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = _(T.subscription)
        verbose_name_plural = _(T.subscriptions)

    def __str__(self):
        return self.email
