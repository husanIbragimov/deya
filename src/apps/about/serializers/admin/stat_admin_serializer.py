from rest_framework import serializers

from apps.about.models import Stat
from apps.common.serializers import TranslatedJSONField


class StatAdminSerializer(serializers.ModelSerializer):
    label = TranslatedJSONField()

    class Meta:
        model = Stat
        fields = ("id", "value", "label", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
