from dataclasses import dataclass
from typing import Optional

from apps.catalog.models import Product
from apps.leads.models import Lead
from apps.leads.services.notifier import LeadNotifier, TelegramLeadNotifier


@dataclass
class CreateLeadDTO:
    type: str
    name: str
    email: str
    phone: str
    message: str = ""
    product: Optional[Product] = None
    consent_personal_data: bool = False
    consent_marketing: bool = False
    source_url: str = ""
    ip_address: Optional[str] = None
    user_agent: str = ""


def create_lead(dto: CreateLeadDTO, notifier: Optional[LeadNotifier] = None) -> Lead:
    notifier = notifier or TelegramLeadNotifier()
    lead = Lead.objects.create(
        type=dto.type,
        name=dto.name,
        email=dto.email,
        phone=dto.phone,
        message=dto.message,
        product=dto.product,
        consent_personal_data=dto.consent_personal_data,
        consent_marketing=dto.consent_marketing,
        source_url=dto.source_url,
        ip_address=dto.ip_address,
        user_agent=dto.user_agent,
    )
    notifier.notify(lead)
    return lead
