from rest_framework import serializers

from apps.careers.models import CareerValue
from apps.common.serializers import TranslatedField


class CareerValueSerializer(serializers.ModelSerializer):
    title = TranslatedField()
    text = TranslatedField()

    class Meta:
        model = CareerValue
        fields = ("id", "title", "text", "image")
