from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.careers.selectors import companies
from apps.careers.serializers import CompanySerializer
from apps.common.pagination import PageNumberPagination


@extend_schema(tags=["Careers"])
class CompanyListView(ListAPIView):
    serializer_class = CompanySerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return companies()
