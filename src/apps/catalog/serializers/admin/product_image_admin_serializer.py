from rest_framework import serializers

from apps.catalog.models import ProductImage


class ProductImageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "product", "image", "alt", "is_main", "sort_order", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
