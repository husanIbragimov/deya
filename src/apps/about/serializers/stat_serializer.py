from rest_framework import serializers

from apps.about.models import Stat
from apps.common.serializers import TranslatedField


class StatSerializer(serializers.ModelSerializer):
    label = TranslatedField()

    class Meta:
        model = Stat
        fields = ("id", "value", "label")
