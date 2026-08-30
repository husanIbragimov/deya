from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.pages.selectors import get_privacy_policy
from apps.pages.serializers import PrivacyPolicySerializer


@extend_schema(tags=["Pages"])
class PrivacyPolicyView(GenericAPIView):
    serializer_class = PrivacyPolicySerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        instance = get_privacy_policy()
        return Response(self.get_serializer(instance).data)
