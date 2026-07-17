from drf_spectacular.utils import extend_schema

from apps.careers.models import CareerValue
from apps.careers.serializers.admin import CareerValueAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Careers Admin"])
class CareerValueAdminListCreateView(AdminListCreateAPI):
    queryset = CareerValue.objects.all()
    serializer_class = CareerValueAdminSerializer


@extend_schema(tags=["Careers Admin"])
class CareerValueAdminDetailView(AdminDetailAPI):
    queryset = CareerValue.objects.all()
    serializer_class = CareerValueAdminSerializer
