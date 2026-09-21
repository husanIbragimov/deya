from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.common.pagination import PageNumberPagination
from apps.partners.selectors import partners
from apps.partners.serializers import PartnerSerializer


@extend_schema(tags=["Partners"])
class PartnerListView(ListAPIView):
    serializer_class = PartnerSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return partners()
