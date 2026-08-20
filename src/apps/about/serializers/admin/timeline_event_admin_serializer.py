from rest_framework import serializers

from apps.about.models import TimelineEvent
from apps.common.serializers import TranslatedJSONField


class TimelineEventAdminSerializer(serializers.ModelSerializer):
    title = TranslatedJSONField()
    description = TranslatedJSONField(required=False)

    class Meta:
        model = TimelineEvent
        fields = ("id", "year", "title", "description", "image", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
