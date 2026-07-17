from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps._auth.models import User
from apps.partners.models import Partner


class PartnerAdminCrudTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)

    def test_create_and_delete_flow(self):
        create_response = self.client.post(
            reverse("partners-admin:partner-admin-list"),
            data={"name": "Acme", "logo": "acme-logo.jpg"},
            format="multipart",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED, create_response.data)
        partner_id = create_response.data["id"]

        delete_response = self.client.delete(reverse("partners-admin:partner-admin-detail", kwargs={"pk": partner_id}))
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Partner.objects.filter(pk=partner_id).exists())
