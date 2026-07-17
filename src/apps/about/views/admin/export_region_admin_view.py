from drf_spectacular.utils import extend_schema

from apps.about.models import ExportRegion
from apps.about.serializers.admin import ExportRegionAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["About Admin"])
class ExportRegionAdminListCreateView(AdminListCreateAPI):
    queryset = ExportRegion.objects.all()
    serializer_class = ExportRegionAdminSerializer


@extend_schema(tags=["About Admin"])
class ExportRegionAdminDetailView(AdminDetailAPI):
    queryset = ExportRegion.objects.all()
    serializer_class = ExportRegionAdminSerializer
