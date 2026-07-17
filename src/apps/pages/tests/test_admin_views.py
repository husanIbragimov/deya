from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps._auth.models import User
from apps.pages.models import SiteSettings


class SiteSettingsAdminViewTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)

    def test_get_creates_default_singleton(self):
        response = self.client.get(reverse("pages-admin:site-settings-admin"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_updates_singleton_in_place(self):
        SiteSettings.objects.create(phone="+998901234567", email="old@example.com")

        response = self.client.put(
            reverse("pages-admin:site-settings-admin"),
            data={"phone": "+998901234567", "email": "new@example.com"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(SiteSettings.objects.count(), 1)
        self.assertEqual(SiteSettings.objects.get().email, "new@example.com")

    def test_non_admin_forbidden(self):
        self.client.force_authenticate(User.objects.create_user(username="visitor", password="pass12345"))
        response = self.client.get(reverse("pages-admin:site-settings-admin"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
