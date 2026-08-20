from rest_framework import serializers

from apps.catalog.models import Category
from apps.common.serializers import TranslatedJSONField


class CategoryAdminSerializer(serializers.ModelSerializer):
    name = TranslatedJSONField()

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "image", "sort_order", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
