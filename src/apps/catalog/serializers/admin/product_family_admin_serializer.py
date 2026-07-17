from rest_framework import serializers

from apps.catalog.models import ProductFamily


class ProductFamilyAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFamily
        fields = ("id", "name", "slug", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
