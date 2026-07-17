from rest_framework import serializers

from apps.blog.models import Post


class PostAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "title", "slug", "excerpt", "cover", "published_at", "is_published", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
