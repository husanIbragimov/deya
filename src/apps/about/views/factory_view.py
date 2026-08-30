from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.about.selectors import get_factory
from apps.about.serializers import FactorySerializer


@extend_schema(tags=["About"])
class FactoryView(GenericAPIView):
    serializer_class = FactorySerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        instance = get_factory()
        return Response(self.get_serializer(instance).data)
