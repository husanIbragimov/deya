from rest_framework import serializers

from apps.about.models import Factory
from apps.common.serializers import TranslatedField


class FactorySerializer(serializers.ModelSerializer):
    title = TranslatedField()
    subtitle = TranslatedField()
    description = TranslatedField()
    subdescription = TranslatedField()

    class Meta:
        model = Factory
        fields = ("title", "subtitle", "description", "subdescription", "image")
