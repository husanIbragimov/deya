from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps._auth.models import User
from apps.leads.models import Lead, NewsletterSubscription


class LeadAdminViewTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)
        self.lead = Lead.objects.create(
            type="contact", name="Ali", email="ali@example.com", phone="+998901234567", consent_personal_data=True
        )

    def test_list(self):
        response = self.client.get(reverse("leads-admin:lead-admin-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve(self):
        response = self.client.get(reverse("leads-admin:lead-admin-detail", kwargs={"pk": self.lead.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Ali")

    def test_status_update(self):
        response = self.client.put(
            reverse("leads-admin:lead-admin-status-update", kwargs={"pk": self.lead.pk}),
            data={"status": "done"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.lead.refresh_from_db()
        self.assertEqual(self.lead.status, "done")

    def test_destroy(self):
        response = self.client.delete(reverse("leads-admin:lead-admin-detail", kwargs={"pk": self.lead.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lead.objects.filter(pk=self.lead.pk).exists())


class SubscriptionAdminViewTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)
        self.subscription = NewsletterSubscription.objects.create(email="a@example.com")

    def test_list(self):
        response = self.client.get(reverse("leads-admin:subscription-admin-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_destroy(self):
        response = self.client.delete(
            reverse("leads-admin:subscription-admin-detail", kwargs={"pk": self.subscription.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(NewsletterSubscription.objects.filter(pk=self.subscription.pk).exists())
