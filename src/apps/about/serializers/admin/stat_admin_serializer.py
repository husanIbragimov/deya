from rest_framework import serializers

from apps.about.models import Stat


class StatAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ("id", "value", "label", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
