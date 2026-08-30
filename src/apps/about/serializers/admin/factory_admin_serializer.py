from rest_framework import serializers

from apps.about.models import Factory
from apps.common.serializers import TranslatedJSONField


class FactoryAdminSerializer(serializers.ModelSerializer):
    title = TranslatedJSONField()
    subtitle = TranslatedJSONField(required=False)
    description = TranslatedJSONField(required=False)
    subdescription = TranslatedJSONField(required=False)

    class Meta:
        model = Factory
        fields = (
            "title",
            "subtitle",
            "description",
            "subdescription",
            "image",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")
