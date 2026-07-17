from rest_framework import serializers

from apps.blog.models import PostBlock


class PostBlockAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostBlock
        fields = ("id", "post", "type", "text", "image", "sort_order", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
