from rest_framework import serializers

from apps.common.serializers import TranslatedField
from apps.pages.models import SiteSettings


class SiteSettingsSerializer(serializers.ModelSerializer):
    address = TranslatedField()
    work_hours = TranslatedField()
    cookie_notice_text = TranslatedField()

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
