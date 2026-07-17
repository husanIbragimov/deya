from drf_spectacular.utils import extend_schema

from apps.about.models import Stat
from apps.about.serializers.admin import StatAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["About Admin"])
class StatAdminListCreateView(AdminListCreateAPI):
    queryset = Stat.objects.all()
    serializer_class = StatAdminSerializer


@extend_schema(tags=["About Admin"])
class StatAdminDetailView(AdminDetailAPI):
    queryset = Stat.objects.all()
    serializer_class = StatAdminSerializer
