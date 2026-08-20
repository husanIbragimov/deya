from rest_framework import serializers

from apps.blog.models import Post
from apps.common.serializers import TranslatedJSONField


class PostAdminSerializer(serializers.ModelSerializer):
    title = TranslatedJSONField()
    excerpt = TranslatedJSONField(required=False)

    class Meta:
        model = Post
        fields = ("id", "title", "slug", "excerpt", "cover", "published_at", "is_published", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
