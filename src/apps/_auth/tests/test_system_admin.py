from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps._auth.models import User
from apps.common.choices import UserRoleChoice


class SystemAdminTests(APITestCase):
    def setUp(self):
        self.system_admin = User.objects.create_user(
            username="sysadmin", password="Sys-Pass-123", role=UserRoleChoice.SYSTEM_ADMIN
        )
        self.admin = User.objects.create_user(username="root-admin", password="Old-Pass-123", role=UserRoleChoice.ADMIN)

    def test_system_admin_can_login_via_api(self):
        response = self.client.post(
            reverse("auth:login_view"), data={"username": "sysadmin", "password": "Sys-Pass-123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertIn("access", response.data)

    def test_system_admin_can_use_user_admin_api(self):
        self.client.force_authenticate(self.system_admin)
        response = self.client.post(
            reverse("user-admin:user-admin-create"),
            data={"first_name": "A", "last_name": "B", "username": "new.user", "password": "Sup3r-Secret-Pass"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    def test_system_admin_can_use_content_admin_api(self):
        self.client.force_authenticate(self.system_admin)
        response = self.client.get(reverse("leads-admin:lead-admin-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

    def test_system_admin_hidden_from_visible_users(self):
        visible = User.objects.visible()
        self.assertNotIn(self.system_admin, visible)
        self.assertIn(self.admin, visible)

    def test_admin_cannot_set_system_admin_password(self):
        self.client.force_authenticate(self.admin)
        url = reverse("user-admin:user-admin-set-password", kwargs={"pk": self.system_admin.pk})
        response = self.client.post(url, data={"password": "New-Strong-Pass-1"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.system_admin.refresh_from_db()
        self.assertTrue(self.system_admin.check_password("Sys-Pass-123"))

    def test_admin_cannot_create_system_admin(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            reverse("user-admin:user-admin-create"),
            data={
                "first_name": "A",
                "last_name": "B",
                "username": "sneaky",
                "password": "Sup3r-Secret-Pass",
                "role": UserRoleChoice.SYSTEM_ADMIN,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("role", response.data)
        self.assertFalse(User.objects.filter(username="sneaky").exists())

    def test_user_cannot_change_own_role(self):
        user = User.objects.create_user(username="regular", password="pass12345", role=UserRoleChoice.USER)
        self.client.force_authenticate(user)
        response = self.client.patch(reverse("user:user_me_view"), data={"role": UserRoleChoice.SYSTEM_ADMIN})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        user.refresh_from_db()
        self.assertEqual(user.role, UserRoleChoice.USER)
