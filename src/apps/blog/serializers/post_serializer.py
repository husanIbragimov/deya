from rest_framework import serializers

from apps.blog.models import Post
from apps.blog.serializers.post_block_serializer import PostBlockSerializer
from apps.common.serializers import TranslatedField


class PostListSerializer(serializers.ModelSerializer):
    title = TranslatedField()
    excerpt = TranslatedField()

    class Meta:
        model = Post
        fields = ("id", "title", "slug", "excerpt", "cover", "published_at")


class PostDetailSerializer(serializers.ModelSerializer):
    title = TranslatedField()
    excerpt = TranslatedField()
    blocks = PostBlockSerializer(many=True, read_only=True)
    other_posts = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "title", "slug", "excerpt", "cover", "published_at", "blocks", "other_posts")

    def get_other_posts(self, obj):
        from apps.blog.selectors import other_posts

        return PostListSerializer(other_posts(obj), many=True, context=self.context).data
