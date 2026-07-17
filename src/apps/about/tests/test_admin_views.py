from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps._auth.models import User
from apps.about.models import Stat


class StatAdminCrudTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)

    def test_create_and_delete_flow(self):
        create_response = self.client.post(
            reverse("about-admin:stat-admin-list"),
            data={"value": "32+", "label": {"ru": "стран", "en": "countries"}},
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED, create_response.data)
        stat_id = create_response.data["id"]

        delete_response = self.client.delete(reverse("about-admin:stat-admin-detail", kwargs={"pk": stat_id}))
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Stat.objects.filter(pk=stat_id).exists())
