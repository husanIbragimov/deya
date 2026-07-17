from rest_framework import serializers

from apps.catalog.models import Flavor


class FlavorAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flavor
        fields = ("id", "name", "slug", "sort_order", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
