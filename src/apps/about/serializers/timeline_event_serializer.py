from rest_framework import serializers

from apps.about.models import TimelineEvent
from apps.common.serializers import TranslatedField


class TimelineEventSerializer(serializers.ModelSerializer):
    title = TranslatedField()
    description = TranslatedField()

    class Meta:
        model = TimelineEvent
        fields = ("id", "year", "title", "description", "image")
