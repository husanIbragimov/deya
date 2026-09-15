from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps._auth.models import User
from apps._auth.serializers.admin import UserAdminCreateSerializer
from apps._auth.serializers.set_password_serializer import SetPasswordSerializer
from apps._auth.services.auth_service import AuthService
from apps.common.base_api import BaseGenericAPI
from apps.common.permissions import IsAdminRole


@extend_schema(tags=["User Admin"])
class UserAdminCreateView(BaseGenericAPI):
    serializer_class = UserAdminCreateSerializer
    permission_classes = (IsAuthenticated, IsAdminRole)

    def post(self, request, *args, **kwargs):
        instance = self.serializer.save(created_by=request.user)
        return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["User Admin"])
class UserAdminSetPasswordView(BaseGenericAPI):
    """
    Lets an admin set a new password for any user without knowing the old one. Logs the
    target user out of every existing session by blacklisting their refresh tokens.
    """

    serializer_class = SetPasswordSerializer
    permission_classes = (IsAuthenticated, IsAdminRole)

    def post(self, request, *args, **kwargs):
        target_user = get_object_or_404(User, pk=kwargs["pk"])
        AuthService.set_password(target_user, self.validate_data["password"])
        return Response({"detail": "Password successfully changed."}, status=status.HTTP_200_OK)
