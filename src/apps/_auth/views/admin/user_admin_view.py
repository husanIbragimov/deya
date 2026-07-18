from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps._auth.serializers.admin import UserAdminCreateSerializer
from apps.common.base_api import BaseGenericAPI
from apps.common.permissions import IsAdminRole


@extend_schema(tags=["User Admin"])
class UserAdminCreateView(BaseGenericAPI):
    serializer_class = UserAdminCreateSerializer
    permission_classes = (IsAuthenticated, IsAdminRole)

    def post(self, request, *args, **kwargs):
        instance = self.serializer.save(created_by=request.user)
        return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)
