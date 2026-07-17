from drf_spectacular.utils import extend_schema

from apps.about.models import TimelineEvent
from apps.about.serializers.admin import TimelineEventAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["About Admin"])
class TimelineEventAdminListCreateView(AdminListCreateAPI):
    queryset = TimelineEvent.objects.all()
    serializer_class = TimelineEventAdminSerializer


@extend_schema(tags=["About Admin"])
class TimelineEventAdminDetailView(AdminDetailAPI):
    queryset = TimelineEvent.objects.all()
    serializer_class = TimelineEventAdminSerializer
