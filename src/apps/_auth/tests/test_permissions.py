from types import SimpleNamespace

from django.contrib.auth.models import AnonymousUser
from django.test import SimpleTestCase

from apps._auth.models import User
from apps.common.choices import UserRoleChoice
from apps.common.permissions import IsAdminRole, IsAdminUser


class IsAdminRoleTests(SimpleTestCase):
    def setUp(self):
        self.permission = IsAdminRole()

    def _request_for(self, user):
        return SimpleNamespace(user=user)

    def test_admin_role_user_has_permission(self):
        user = User(username="admin", role=UserRoleChoice.ADMIN)
        self.assertTrue(self.permission.has_permission(self._request_for(user), None))

    def test_regular_role_user_denied(self):
        user = User(username="regular", role=UserRoleChoice.USER)
        self.assertFalse(self.permission.has_permission(self._request_for(user), None))

    def test_anonymous_user_denied(self):
        self.assertFalse(self.permission.has_permission(self._request_for(AnonymousUser()), None))

    def test_system_admin_role_user_has_permission(self):
        user = User(username="sysadmin", role=UserRoleChoice.SYSTEM_ADMIN)
        self.assertTrue(self.permission.has_permission(self._request_for(user), None))


class IsAdminUserTests(SimpleTestCase):
    def setUp(self):
        self.permission = IsAdminUser()

    def _request_for(self, user):
        return SimpleNamespace(user=user)

    def test_staff_user_has_permission(self):
        user = User(username="staff", role=UserRoleChoice.USER, is_staff=True)
        self.assertTrue(self.permission.has_permission(self._request_for(user), None))

    def test_system_admin_without_is_staff_has_permission(self):
        user = User(username="sysadmin", role=UserRoleChoice.SYSTEM_ADMIN, is_staff=False)
        self.assertTrue(self.permission.has_permission(self._request_for(user), None))

    def test_admin_role_without_is_staff_denied(self):
        user = User(username="admin", role=UserRoleChoice.ADMIN, is_staff=False)
        self.assertFalse(self.permission.has_permission(self._request_for(user), None))

    def test_anonymous_user_denied(self):
        self.assertFalse(self.permission.has_permission(self._request_for(AnonymousUser()), None))
