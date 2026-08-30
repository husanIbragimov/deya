from drf_spectacular.utils import extend_schema

from apps.about.models import ProductInfo
from apps.about.serializers.admin import ProductInfoAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["About Admin"])
class ProductInfoAdminListCreateView(AdminListCreateAPI):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoAdminSerializer


@extend_schema(tags=["About Admin"])
class ProductInfoAdminDetailView(AdminDetailAPI):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoAdminSerializer
