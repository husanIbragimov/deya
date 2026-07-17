from rest_framework import serializers

from apps.about.models import ExportRegion
from apps.common.serializers import TranslatedField


class ExportRegionSerializer(serializers.ModelSerializer):
    name = TranslatedField()

    class Meta:
        model = ExportRegion
        fields = ("id", "name", "position_x", "position_y")
