from rest_framework import serializers

from apps.catalog.models import Weight


class WeightAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weight
        fields = ("id", "value", "unit", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
