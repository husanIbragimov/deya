from drf_spectacular.utils import extend_schema

from apps.catalog.models import ProductFamily
from apps.catalog.serializers.admin import ProductFamilyAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Catalog Admin"])
class ProductFamilyAdminListCreateView(AdminListCreateAPI):
    queryset = ProductFamily.objects.all().order_by("name")
    serializer_class = ProductFamilyAdminSerializer


@extend_schema(tags=["Catalog Admin"])
class ProductFamilyAdminDetailView(AdminDetailAPI):
    queryset = ProductFamily.objects.all()
    serializer_class = ProductFamilyAdminSerializer
