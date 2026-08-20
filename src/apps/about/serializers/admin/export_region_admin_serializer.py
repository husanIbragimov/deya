from rest_framework import serializers

from apps.about.models import ExportRegion
from apps.common.serializers import TranslatedJSONField


class ExportRegionAdminSerializer(serializers.ModelSerializer):
    name = TranslatedJSONField()

    class Meta:
        model = ExportRegion
        fields = ("id", "name", "position_x", "position_y", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
