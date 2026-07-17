from drf_spectacular.utils import extend_schema

from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI
from apps.partners.models import Certificate
from apps.partners.serializers.admin import CertificateAdminSerializer


@extend_schema(tags=["Partners Admin"])
class CertificateAdminListCreateView(AdminListCreateAPI):
    queryset = Certificate.objects.all()
    serializer_class = CertificateAdminSerializer


@extend_schema(tags=["Partners Admin"])
class CertificateAdminDetailView(AdminDetailAPI):
    queryset = Certificate.objects.all()
    serializer_class = CertificateAdminSerializer
