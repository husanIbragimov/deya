from rest_framework import serializers

from apps.common.serializers import TranslatedJSONField
from apps.pages.models import Banner


class BannerAdminSerializer(serializers.ModelSerializer):
    title = TranslatedJSONField()
    subtitle = TranslatedJSONField(required=False)
    cta_label = TranslatedJSONField(required=False, allow_null=True)

    class Meta:
        model = Banner
        fields = ("id", "type", "title", "subtitle", "image", "cta_label", "cta_url", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
        extra_kwargs = {"cta_url": {"required": False, "allow_null": True}}
