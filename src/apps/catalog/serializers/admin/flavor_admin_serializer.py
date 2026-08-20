from rest_framework import serializers

from apps.catalog.models import Flavor
from apps.common.serializers import TranslatedJSONField


class FlavorAdminSerializer(serializers.ModelSerializer):
    name = TranslatedJSONField()

    class Meta:
        model = Flavor
        fields = ("id", "name", "slug", "sort_order", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
