from rest_framework import serializers

from apps.about.models import TimelineEvent


class TimelineEventAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineEvent
        fields = ("id", "year", "title", "description", "image", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
