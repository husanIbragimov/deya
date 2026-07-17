from unittest.mock import patch

from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.leads.models import Lead, NewsletterSubscription


class LeadCreateViewTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.patcher = patch("apps.leads.services.notifier.notifyAdminTask.delay")
        self.mock_delay = self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def _payload(self, **overrides):
        payload = {
            "type": "contact",
            "name": "Ali",
            "email": "ali@example.com",
            "phone": "+998901234567",
            "consent_personal_data": True,
        }
        payload.update(overrides)
        return payload

    def test_creates_lead_and_dispatches_notification(self):
        response = self.client.post(reverse("leads:lead-create"), data=self._payload(), format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Lead.objects.count(), 1)
        self.mock_delay.assert_called_once()

    def test_missing_consent_is_rejected(self):
        response = self.client.post(
            reverse("leads:lead-create"), data=self._payload(consent_personal_data=False), format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lead.objects.count(), 0)

    def test_sixth_request_within_an_hour_is_throttled(self):
        for _ in range(5):
            response = self.client.post(reverse("leads:lead-create"), data=self._payload(), format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(reverse("leads:lead-create"), data=self._payload(), format="json")
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class SubscriptionCreateViewTests(APITestCase):
    def setUp(self):
        cache.clear()

    def test_creates_subscription(self):
        response = self.client.post(reverse("leads:subscription-create"), data={"email": "a@example.com"})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NewsletterSubscription.objects.count(), 1)

    def test_fourth_request_within_an_hour_is_throttled(self):
        for i in range(3):
            response = self.client.post(reverse("leads:subscription-create"), data={"email": f"user{i}@example.com"})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(reverse("leads:subscription-create"), data={"email": "user4@example.com"})
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class UnsubscribeViewTests(APITestCase):
    def test_deactivates_subscription(self):
        subscription = NewsletterSubscription.objects.create(email="x@example.com")

        response = self.client.get(
            reverse("leads:subscription-unsubscribe", kwargs={"token": subscription.unsubscribe_token})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        subscription.refresh_from_db()
        self.assertFalse(subscription.is_active)

    def test_invalid_token_returns_404(self):
        response = self.client.get(
            reverse("leads:subscription-unsubscribe", kwargs={"token": "00000000-0000-0000-0000-000000000000"})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
