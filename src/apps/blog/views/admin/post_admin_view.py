from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response

from apps.blog.models import Post
from apps.blog.serializers.admin import PostAdminSerializer
from apps.blog.tasks import sendBlogNewsletterTask
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI
from apps.common.pagination import PageNumberPagination


@extend_schema(tags=["Blog Admin"])
class PostAdminListCreateView(AdminListCreateAPI):
    queryset = Post.objects.all().order_by("-published_at")
    serializer_class = PostAdminSerializer
    pagination_class = PageNumberPagination

    def post(self, request, *args, **kwargs):
        instance = self.serializer.save(created_by=request.user)
        if instance.is_published:
            sendBlogNewsletterTask.delay(post_id=instance.id)
        return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Blog Admin"])
class PostAdminDetailView(AdminDetailAPI):
    queryset = Post.objects.all()
    serializer_class = PostAdminSerializer
