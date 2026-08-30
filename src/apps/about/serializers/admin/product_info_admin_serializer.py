from rest_framework import serializers

from apps.about.models import ProductInfo
from apps.common.serializers import TranslatedJSONField


class ProductInfoAdminSerializer(serializers.ModelSerializer):
    title = TranslatedJSONField()
    description = TranslatedJSONField(required=False)

    class Meta:
        model = ProductInfo
        fields = ("id", "title", "description", "image", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
