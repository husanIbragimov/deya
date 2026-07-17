from django.test import TestCase

from apps.leads.models import Lead, NewsletterSubscription
from apps.leads.services import CreateLeadDTO, create_lead, subscribe, unsubscribe
from apps.leads.services.notifier import LeadNotifier


class FakeNotifier(LeadNotifier):
    def __init__(self):
        self.notified = []

    def notify(self, lead):
        self.notified.append(lead)


class CreateLeadServiceTests(TestCase):
    def test_saves_lead_and_notifies(self):
        notifier = FakeNotifier()
        dto = CreateLeadDTO(
            type="contact",
            name="Ali",
            email="ali@example.com",
            phone="+998901234567",
            consent_personal_data=True,
        )

        lead = create_lead(dto, notifier=notifier)

        self.assertEqual(Lead.objects.count(), 1)
        self.assertEqual(lead.name, "Ali")
        self.assertEqual(notifier.notified, [lead])


class SubscribeServiceTests(TestCase):
    def test_creates_new_subscription(self):
        subscription = subscribe("new@example.com")
        self.assertTrue(subscription.is_active)
        self.assertEqual(NewsletterSubscription.objects.count(), 1)

    def test_is_idempotent_for_existing_active_subscription(self):
        subscribe("dup@example.com")
        subscribe("dup@example.com")
        self.assertEqual(NewsletterSubscription.objects.count(), 1)

    def test_reactivates_previously_unsubscribed_email(self):
        subscription = subscribe("was-inactive@example.com")
        subscription.is_active = False
        subscription.save(update_fields=["is_active"])

        reactivated = subscribe("was-inactive@example.com")

        self.assertTrue(reactivated.is_active)
        self.assertEqual(NewsletterSubscription.objects.count(), 1)


class UnsubscribeServiceTests(TestCase):
    def test_deactivates_subscription_by_token(self):
        subscription = NewsletterSubscription.objects.create(email="active@example.com")

        result = unsubscribe(str(subscription.unsubscribe_token))

        self.assertFalse(result.is_active)

    def test_invalid_token_raises(self):
        from apps.common.response import ExceptionResponse

        with self.assertRaises(ExceptionResponse):
            unsubscribe("00000000-0000-0000-0000-000000000000")
