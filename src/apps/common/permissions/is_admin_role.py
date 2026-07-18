from rest_framework.permissions import BasePermission

from apps.common.choices import UserRoleChoice


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.role == UserRoleChoice.ADMIN)
