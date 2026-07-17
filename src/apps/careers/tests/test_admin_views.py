from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps._auth.models import User
from apps.careers.models import CareerValue
from apps.careers.tests.helpers import tr


class CareerValueAdminCrudTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)

    def test_create_and_delete_flow(self):
        create_response = self.client.post(
            reverse("careers-admin:career-value-admin-list"),
            data={"title": tr("Value"), "text": tr("Text")},
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED, create_response.data)
        value_id = create_response.data["id"]

        delete_response = self.client.delete(
            reverse("careers-admin:career-value-admin-detail", kwargs={"pk": value_id})
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CareerValue.objects.filter(pk=value_id).exists())
