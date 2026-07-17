from drf_spectacular.utils import extend_schema

from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI
from apps.pages.models import StaticPage
from apps.pages.serializers.admin import StaticPageAdminSerializer


@extend_schema(tags=["Pages Admin"])
class StaticPageAdminListCreateView(AdminListCreateAPI):
    queryset = StaticPage.objects.all()
    serializer_class = StaticPageAdminSerializer


@extend_schema(tags=["Pages Admin"])
class StaticPageAdminDetailView(AdminDetailAPI):
    queryset = StaticPage.objects.all()
    serializer_class = StaticPageAdminSerializer
