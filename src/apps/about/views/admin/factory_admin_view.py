from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.about.selectors import get_factory
from apps.about.serializers.admin import FactoryAdminSerializer
from apps.common.base_api import BaseGenericUpdateAPI


@extend_schema(tags=["About Admin"])
class FactoryAdminView(BaseGenericUpdateAPI):
    """Singleton resource: GET reads it, PUT/PATCH update it. No list/create/delete."""

    serializer_class = FactoryAdminSerializer
    permission_classes = (IsAdminUser,)

    def get_object(self):
        return get_factory()

    def get(self, request, *args, **kwargs):
        return Response(self.get_serializer(self.get_object()).data)

    def put(self, request, *args, **kwargs):
        instance = self.serializer.save()
        return Response(self.get_serializer(instance).data)

    def patch(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)
