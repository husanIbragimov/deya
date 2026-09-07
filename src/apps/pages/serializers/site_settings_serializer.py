from rest_framework import serializers

from apps.common.serializers import TranslatedJSONField
from apps.pages.models import SiteSettings


class SiteSettingsSerializer(serializers.ModelSerializer):
    address = TranslatedJSONField(read_only=True)
    work_hours = TranslatedJSONField(read_only=True)
    cookie_notice_text = TranslatedJSONField(read_only=True)

    class Meta:
        model = SiteSettings
        fields = (
            "phone",
            "hotline",
            "email",
            "address",
            "work_hours",
            "yandex_map_url",
            "instagram_url",
            "telegram_url",
            "catalog_file",
            "cookie_notice_text",
        )
