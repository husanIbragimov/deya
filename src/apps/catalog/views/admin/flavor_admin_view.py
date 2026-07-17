from drf_spectacular.utils import extend_schema

from apps.catalog.models import Flavor
from apps.catalog.serializers.admin import FlavorAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Catalog Admin"])
class FlavorAdminListCreateView(AdminListCreateAPI):
    queryset = Flavor.objects.all().order_by("sort_order", "id")
    serializer_class = FlavorAdminSerializer


@extend_schema(tags=["Catalog Admin"])
class FlavorAdminDetailView(AdminDetailAPI):
    queryset = Flavor.objects.all()
    serializer_class = FlavorAdminSerializer
