from drf_spectacular.utils import extend_schema

from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI
from apps.partners.models import Partner
from apps.partners.serializers.admin import PartnerAdminSerializer


@extend_schema(tags=["Partners Admin"])
class PartnerAdminListCreateView(AdminListCreateAPI):
    queryset = Partner.objects.all().order_by("name")
    serializer_class = PartnerAdminSerializer


@extend_schema(tags=["Partners Admin"])
class PartnerAdminDetailView(AdminDetailAPI):
    queryset = Partner.objects.all()
    serializer_class = PartnerAdminSerializer
