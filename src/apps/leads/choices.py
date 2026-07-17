from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _


class LeadTypeChoice(models.TextChoices):
    PARTNER = "partner", _(T.lead_type_partner)
    SALES = "sales", _(T.lead_type_sales)
    CONTACT = "contact", _(T.lead_type_contact)


class LeadStatusChoice(models.TextChoices):
    NEW = "new", _(T.lead_status_new)
    IN_PROGRESS = "in_progress", _(T.in_progress)
    DONE = "done", _(T.done)
