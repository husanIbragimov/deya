from rest_framework import serializers

from apps.blog.models import PostBlock
from apps.common.serializers import TranslatedField


class PostBlockSerializer(serializers.ModelSerializer):
    text = TranslatedField()

    class Meta:
        model = PostBlock
        fields = ("id", "type", "text", "image", "sort_order")
