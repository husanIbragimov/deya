from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt.tokens import RefreshToken

from apps._auth.models import User
from apps.common.choices import UserRoleChoice


class SetPasswordViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("user:set-password")
        self.user = User.objects.create_user(username="regular", password="Old-Pass-123", role=UserRoleChoice.USER)

    def test_anonymous_cannot_set_password(self):
        response = self.client.post(self.url, data={"password": "New-Strong-Pass-1"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_set_own_password_without_old_password(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(self.url, data={"password": "New-Strong-Pass-1"})

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("New-Strong-Pass-1"))

    def test_set_password_blacklists_existing_sessions(self):
        refresh = RefreshToken.for_user(self.user)
        outstanding_token = OutstandingToken.objects.get(jti=refresh["jti"])
        self.client.force_authenticate(self.user)

        response = self.client.post(self.url, data={"password": "New-Strong-Pass-1"})

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertTrue(BlacklistedToken.objects.filter(token=outstanding_token).exists())

    def test_weak_password_rejected(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(self.url, data={"password": "short"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("Old-Pass-123"))


class AdminSetPasswordViewTests(APITestCase):
    def setUp(self):
        self.target = User.objects.create_user(username="target", password="Old-Pass-123", role=UserRoleChoice.USER)
        self.url = reverse("user-admin:user-admin-set-password", kwargs={"pk": self.target.pk})

    def test_anonymous_forbidden(self):
        response = self.client.post(self.url, data={"password": "New-Strong-Pass-1"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_regular_user_forbidden(self):
        regular = User.objects.create_user(username="regular", password="Old-Pass-123", role=UserRoleChoice.USER)
        self.client.force_authenticate(regular)

        response = self.client.post(self.url, data={"password": "New-Strong-Pass-1"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_set_other_user_password(self):
        admin = User.objects.create_user(username="root-admin", password="Old-Pass-123", role=UserRoleChoice.ADMIN)
        refresh = RefreshToken.for_user(self.target)
        outstanding_token = OutstandingToken.objects.get(jti=refresh["jti"])
        self.client.force_authenticate(admin)

        response = self.client.post(self.url, data={"password": "New-Strong-Pass-1"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.target.refresh_from_db()
        self.assertTrue(self.target.check_password("New-Strong-Pass-1"))
        self.assertTrue(BlacklistedToken.objects.filter(token=outstanding_token).exists())

    def test_admin_set_password_nonexistent_user_returns_404(self):
        admin = User.objects.create_user(username="root-admin", password="Old-Pass-123", role=UserRoleChoice.ADMIN)
        self.client.force_authenticate(admin)
        url = reverse("user-admin:user-admin-set-password", kwargs={"pk": 999999})

        response = self.client.post(url, data={"password": "New-Strong-Pass-1"})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
