from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from apps.pages.models import PrivacyPolicy
from apps.pages.selectors import privacy_policies
from apps.pages.serializers import PrivacyPolicySerializer


@extend_schema(tags=["Pages"])
class PrivacyPolicyListView(ListAPIView):
    serializer_class = PrivacyPolicySerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return privacy_policies()


@extend_schema(tags=["Pages"])
class PrivacyPolicyDetailView(RetrieveAPIView):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer
    permission_classes = (AllowAny,)
    lookup_field = "slug"
