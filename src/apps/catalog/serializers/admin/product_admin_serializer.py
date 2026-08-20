from rest_framework import serializers

from apps.catalog.models import Product
from apps.common.serializers import TranslatedJSONField


class ProductAdminSerializer(serializers.ModelSerializer):
    name = TranslatedJSONField()
    description = TranslatedJSONField(required=False)

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "family",
            "flavor",
            "name",
            "slug",
            "description",
            "code",
            "box_weight",
            "shelf_life_months",
            "weights",
            "badge",
            "is_featured",
            "related_products",
            "sort_order",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
