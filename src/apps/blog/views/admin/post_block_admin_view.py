from drf_spectacular.utils import extend_schema

from apps.blog.models import PostBlock
from apps.blog.serializers.admin import PostBlockAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Blog Admin"])
class PostBlockAdminListCreateView(AdminListCreateAPI):
    queryset = PostBlock.objects.select_related("post").all().order_by("sort_order", "id")
    serializer_class = PostBlockAdminSerializer


@extend_schema(tags=["Blog Admin"])
class PostBlockAdminDetailView(AdminDetailAPI):
    queryset = PostBlock.objects.select_related("post").all()
    serializer_class = PostBlockAdminSerializer
