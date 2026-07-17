from drf_spectacular.utils import extend_schema

from apps.about.models import HomeSlide
from apps.about.serializers.admin import HomeSlideAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["About Admin"])
class HomeSlideAdminListCreateView(AdminListCreateAPI):
    queryset = HomeSlide.objects.all()
    serializer_class = HomeSlideAdminSerializer


@extend_schema(tags=["About Admin"])
class HomeSlideAdminDetailView(AdminDetailAPI):
    queryset = HomeSlide.objects.all()
    serializer_class = HomeSlideAdminSerializer
