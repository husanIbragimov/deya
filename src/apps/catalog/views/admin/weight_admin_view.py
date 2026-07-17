from drf_spectacular.utils import extend_schema

from apps.catalog.models import Weight
from apps.catalog.serializers.admin import WeightAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Catalog Admin"])
class WeightAdminListCreateView(AdminListCreateAPI):
    queryset = Weight.objects.all().order_by("unit", "value")
    serializer_class = WeightAdminSerializer


@extend_schema(tags=["Catalog Admin"])
class WeightAdminDetailView(AdminDetailAPI):
    queryset = Weight.objects.all()
    serializer_class = WeightAdminSerializer
