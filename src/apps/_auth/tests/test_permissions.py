from types import SimpleNamespace

from django.contrib.auth.models import AnonymousUser
from django.test import SimpleTestCase

from apps._auth.models import User
from apps.common.choices import UserRoleChoice
from apps.common.permissions import IsAdminRole


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
