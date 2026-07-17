from drf_spectacular.utils import extend_schema

from apps.catalog.models import Category
from apps.catalog.serializers.admin import CategoryAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Catalog Admin"])
class CategoryAdminListCreateView(AdminListCreateAPI):
    queryset = Category.objects.all().order_by("sort_order", "id")
    serializer_class = CategoryAdminSerializer


@extend_schema(tags=["Catalog Admin"])
class CategoryAdminDetailView(AdminDetailAPI):
    queryset = Category.objects.all()
    serializer_class = CategoryAdminSerializer
