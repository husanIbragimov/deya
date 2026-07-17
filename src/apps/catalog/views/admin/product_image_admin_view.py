from drf_spectacular.utils import extend_schema

from apps.catalog.models import ProductImage
from apps.catalog.serializers.admin import ProductImageAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Catalog Admin"])
class ProductImageAdminListCreateView(AdminListCreateAPI):
    queryset = ProductImage.objects.select_related("product").all().order_by("sort_order", "id")
    serializer_class = ProductImageAdminSerializer


@extend_schema(tags=["Catalog Admin"])
class ProductImageAdminDetailView(AdminDetailAPI):
    queryset = ProductImage.objects.select_related("product").all()
    serializer_class = ProductImageAdminSerializer
