from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.pages.selectors import get_site_settings
from apps.pages.serializers import SiteSettingsSerializer


@extend_schema(tags=["Pages"])
class SiteSettingsView(GenericAPIView):
    serializer_class = SiteSettingsSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        instance = get_site_settings()
        return Response(self.get_serializer(instance).data)
