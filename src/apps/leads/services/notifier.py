from abc import ABC, abstractmethod

from apps.leads.models import Lead
from apps.logger.tasks.notify_admin_task import notifyAdminTask


class LeadNotifier(ABC):
    @abstractmethod
    def notify(self, lead: Lead) -> None:
        ...


class TelegramLeadNotifier(LeadNotifier):
    def notify(self, lead: Lead) -> None:
        message = (
            f"Type: {lead.get_type_display()}\n"
            f"Name: {lead.name}\n"
            f"Phone: {lead.phone}\n"
            f"Email: {lead.email}\n"
            f"Message: {lead.message or '-'}"
        )
        notifyAdminTask.delay(message=message, _from="Leads")
