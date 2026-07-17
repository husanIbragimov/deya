from rest_framework import serializers

from apps.catalog.models import Flavor
from apps.common.serializers import TranslatedField


class FlavorSerializer(serializers.ModelSerializer):
    name = TranslatedField()

    class Meta:
        model = Flavor
        fields = ("id", "name", "slug")
