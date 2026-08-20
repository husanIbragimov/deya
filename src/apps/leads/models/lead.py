from django.db import models

from apps.common.choices import choices_help_text
from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel
from apps.common.utils.phone_validator import phone_validator
from apps.leads.choices import LeadStatusChoice, LeadTypeChoice


class Lead(BaseModel):
    type = models.CharField(
        max_length=16,
        choices=LeadTypeChoice.choices,
        db_index=True,
        verbose_name=_(T.lead_type),
        help_text=choices_help_text(LeadTypeChoice),
    )
    name = models.CharField(max_length=150, verbose_name=_(T.common_name))
    email = models.EmailField(verbose_name=_(T.email))
    phone = models.CharField(max_length=20, validators=[phone_validator], verbose_name=_(T.phone_number))
    message = models.TextField(blank=True, verbose_name=_(T.message))
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leads",
        verbose_name=_(T.product),
    )
    consent_personal_data = models.BooleanField(default=False, verbose_name=_(T.consent_personal_data))
    consent_marketing = models.BooleanField(default=False, verbose_name=_(T.consent_marketing))
    status = models.CharField(
        max_length=16,
        choices=LeadStatusChoice.choices,
        default=LeadStatusChoice.NEW,
        db_index=True,
        verbose_name=_(T.status),
        help_text=choices_help_text(LeadStatusChoice),
    )
    source_url = models.URLField(blank=True, verbose_name=_(T.source_url))
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name=_(T.ip_address))
    user_agent = models.CharField(max_length=500, blank=True, verbose_name=_(T.user_agent))

    class Meta:
        ordering = ("-id",)
        verbose_name = _(T.lead)
        verbose_name_plural = _(T.leads)
        indexes = [
            models.Index(fields=("type", "status", "-created_at")),
        ]

    def __str__(self):
        return f"{self.get_type_display()}: {self.name}"
