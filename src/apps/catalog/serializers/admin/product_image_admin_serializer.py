from rest_framework import serializers

from apps.catalog.models import ProductImage
from apps.common.serializers import TranslatedJSONField


class ProductImageAdminSerializer(serializers.ModelSerializer):
    alt = TranslatedJSONField(required=False)

    class Meta:
        model = ProductImage
        fields = ("id", "product", "image", "alt", "is_main", "sort_order", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
