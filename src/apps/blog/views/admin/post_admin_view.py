from drf_spectacular.utils import extend_schema

from apps.blog.models import Post
from apps.blog.serializers.admin import PostAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Blog Admin"])
class PostAdminListCreateView(AdminListCreateAPI):
    queryset = Post.objects.all().order_by("-published_at")
    serializer_class = PostAdminSerializer


@extend_schema(tags=["Blog Admin"])
class PostAdminDetailView(AdminDetailAPI):
    queryset = Post.objects.all()
    serializer_class = PostAdminSerializer
