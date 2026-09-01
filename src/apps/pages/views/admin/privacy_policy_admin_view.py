from drf_spectacular.utils import extend_schema

from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI
from apps.pages.models import PrivacyPolicy
from apps.pages.serializers.admin import PrivacyPolicyAdminSerializer


@extend_schema(tags=["Pages Admin"])
class PrivacyPolicyAdminListCreateView(AdminListCreateAPI):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicyAdminSerializer


@extend_schema(tags=["Pages Admin"])
class PrivacyPolicyAdminDetailView(AdminDetailAPI):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicyAdminSerializer
    lookup_field = "slug"
