from rest_framework import serializers

from apps.catalog.models import Weight


class WeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weight
        fields = ("id", "value", "unit")
