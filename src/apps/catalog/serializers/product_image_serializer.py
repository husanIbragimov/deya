from rest_framework import serializers

from apps.catalog.models import ProductImage
from apps.common.serializers import TranslatedField


class ProductImageSerializer(serializers.ModelSerializer):
    alt = TranslatedField()

    class Meta:
        model = ProductImage
        fields = ("id", "image", "alt", "is_main", "sort_order")
