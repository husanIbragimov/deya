from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.pages.selectors import banners
from apps.pages.serializers import BannerSerializer


@extend_schema(
    tags=["Pages"],
    parameters=[
        OpenApiParameter(
            name="type",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Filter banners by page type, e.g. `partner`.",
        )
    ],
)
class BannerListView(ListAPIView):
    serializer_class = BannerSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return banners(type_=self.request.query_params.get("type"))
