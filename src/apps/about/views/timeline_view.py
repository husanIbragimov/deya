from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.about.selectors import timeline_events
from apps.about.serializers import TimelineEventSerializer


@extend_schema(tags=["About"])
class TimelineListView(ListAPIView):
    serializer_class = TimelineEventSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return timeline_events()
