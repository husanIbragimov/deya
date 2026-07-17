from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from apps.blog.selectors import get_post_by_slug, published_posts
from apps.blog.serializers import PostDetailSerializer, PostListSerializer
from apps.common.pagination import PageNumberPagination


@extend_schema(tags=["Blog"])
class PostListView(ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return published_posts()


@extend_schema(tags=["Blog"])
class PostDetailView(RetrieveAPIView):
    serializer_class = PostDetailSerializer
    permission_classes = (AllowAny,)
    lookup_field = "slug"

    def get_object(self):
        return get_post_by_slug(self.kwargs["slug"])
