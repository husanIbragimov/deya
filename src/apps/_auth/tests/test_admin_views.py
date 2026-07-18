from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps._auth.models import User
from apps.common.choices import UserRoleChoice


class UserAdminCreateViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("user-admin:user-admin-create")
        self.valid_payload = {
            "first_name": "Aziz",
            "last_name": "Karimov",
            "username": "aziz.karimov",
            "password": "Sup3r-Secret-Pass",
        }

    def test_anonymous_cannot_create(self):
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_regular_role_user_forbidden(self):
        user = User.objects.create_user(username="regular", password="pass12345", role=UserRoleChoice.USER)
        self.client.force_authenticate(user)
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_role_without_is_staff_can_create(self):
        admin = User.objects.create_user(
            username="root-admin", password="pass12345", role=UserRoleChoice.ADMIN, is_staff=False
        )
        self.client.force_authenticate(admin)
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    def test_create_user_success(self):
        admin = User.objects.create_user(username="root-admin", password="pass12345", role=UserRoleChoice.ADMIN)
        self.client.force_authenticate(admin)

        response = self.client.post(self.url, data=self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data["username"], "aziz.karimov")
        self.assertEqual(response.data["first_name"], "Aziz")
        self.assertEqual(response.data["last_name"], "Karimov")
        self.assertEqual(response.data["role"], UserRoleChoice.USER)
        self.assertNotIn("password", response.data)

        created = User.objects.get(username="aziz.karimov")
        self.assertTrue(created.check_password("Sup3r-Secret-Pass"))
        self.assertEqual(created.created_by, admin)
        self.assertFalse(created.is_staff)

    def test_duplicate_username_rejected(self):
        admin = User.objects.create_user(username="root-admin", password="pass12345", role=UserRoleChoice.ADMIN)
        self.client.force_authenticate(admin)
        User.objects.create_user(username="aziz.karimov", password="pass12345")

        response = self.client.post(self.url, data=self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_missing_first_name_rejected(self):
        admin = User.objects.create_user(username="root-admin", password="pass12345", role=UserRoleChoice.ADMIN)
        self.client.force_authenticate(admin)
        payload = {**self.valid_payload}
        del payload["first_name"]

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", response.data)
