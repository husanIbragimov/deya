from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.about.models import Factory
from apps.about.selectors import get_factory
from apps.about.serializers.admin import FactoryAdminSerializer
from apps.common.base_api import BaseGenericUpdateAPI
from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.response import ExceptionResponse, ResponseCode


@extend_schema(tags=["About Admin"])
class FactoryAdminView(BaseGenericUpdateAPI):
    """Singleton resource: GET reads it, POST creates it if missing, PUT/PATCH update it. No list/delete."""

    serializer_class = FactoryAdminSerializer
    permission_classes = (IsAdminUser,)

    def get_object(self):
        return get_factory()

    def perform_check(self, request, *args, **kwargs):
        if request.method == "POST":
            self._serializer = self.serializer_class(data=request.data)
            self._serializer.is_valid(raise_exception=True)
            self._validate_data = self._serializer.validated_data
            return self._validate_data
        return super().perform_check(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return Response(self.get_serializer(self.get_object()).data)

    def post(self, request, *args, **kwargs):
        if Factory.objects.filter(pk=1).exists():
            raise ExceptionResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                response_code=ResponseCode.FACTORY_ALREADY_EXISTS,
                detail=str(_(T.factory_already_exists_message)),
            )
        instance = self.serializer.save(created_by=request.user)
        return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        instance = self.serializer.save()
        return Response(self.get_serializer(instance).data)

    def patch(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)
