from drf_spectacular.utils import extend_schema

from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI
from apps.pages.models import Banner
from apps.pages.serializers.admin import BannerAdminSerializer


@extend_schema(tags=["Pages Admin"])
class BannerAdminListCreateView(AdminListCreateAPI):
    queryset = Banner.objects.all()
    serializer_class = BannerAdminSerializer


@extend_schema(tags=["Pages Admin"])
class BannerAdminDetailView(AdminDetailAPI):
    queryset = Banner.objects.all()
    serializer_class = BannerAdminSerializer
