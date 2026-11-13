from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAdminUser as DRFIsAdminUser

from apps.common.choices import UserRoleChoice

ADMIN_ROLES = (UserRoleChoice.ADMIN, UserRoleChoice.SYSTEM_ADMIN)


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.role in ADMIN_ROLES)


class IsAdminUser(DRFIsAdminUser):
    """DRF's IsAdminUser (is_staff) that also lets SYSTEM_ADMIN users through."""

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True
        user = request.user
        return bool(user and user.is_authenticated and user.role == UserRoleChoice.SYSTEM_ADMIN)
