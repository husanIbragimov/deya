from rest_framework import serializers

from apps.careers.models import CareerValue
from apps.common.serializers import TranslatedJSONField


class CareerValueAdminSerializer(serializers.ModelSerializer):
    title = TranslatedJSONField()
    text = TranslatedJSONField()

    class Meta:
        model = CareerValue
        fields = ("id", "title", "text", "image", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
