from rest_framework import serializers

from apps.about.models import HomeSlide
from apps.common.serializers import TranslatedJSONField


class HomeSlideAdminSerializer(serializers.ModelSerializer):
    title = TranslatedJSONField()
    subtitle = TranslatedJSONField(required=False)
    cta_label = TranslatedJSONField(required=False)

    class Meta:
        model = HomeSlide
        fields = ("id", "title", "subtitle", "image", "cta_label", "cta_url", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
