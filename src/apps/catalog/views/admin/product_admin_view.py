from drf_spectacular.utils import extend_schema

from apps.catalog.models import Product
from apps.catalog.serializers.admin import ProductAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI
from apps.common.pagination import PageNumberPagination


@extend_schema(tags=["Catalog Admin"])
class ProductAdminListCreateView(AdminListCreateAPI):
    queryset = Product.objects.select_related("category", "family", "flavor").all().order_by("sort_order", "id")
    serializer_class = ProductAdminSerializer
    pagination_class = PageNumberPagination


@extend_schema(tags=["Catalog Admin"])
class ProductAdminDetailView(AdminDetailAPI):
    queryset = Product.objects.select_related("category", "family", "flavor").all()
    serializer_class = ProductAdminSerializer
