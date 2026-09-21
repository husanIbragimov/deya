from drf_spectacular.utils import extend_schema

from apps.careers.models import Company
from apps.careers.serializers.admin import CompanyAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI
from apps.common.pagination import PageNumberPagination


@extend_schema(tags=["Careers Admin"])
class CompanyAdminListCreateView(AdminListCreateAPI):
    queryset = Company.objects.all().order_by("name")
    serializer_class = CompanyAdminSerializer
    pagination_class = PageNumberPagination


@extend_schema(tags=["Careers Admin"])
class CompanyAdminDetailView(AdminDetailAPI):
    queryset = Company.objects.all()
    serializer_class = CompanyAdminSerializer
