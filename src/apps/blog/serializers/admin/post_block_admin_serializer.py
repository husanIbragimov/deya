from rest_framework import serializers

from apps.blog.models import PostBlock
from apps.common.serializers import TranslatedJSONField


class PostBlockAdminSerializer(serializers.ModelSerializer):
    text = TranslatedJSONField(required=False)

    class Meta:
        model = PostBlock
        fields = ("id", "post", "type", "text", "image", "sort_order", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
