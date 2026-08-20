from rest_framework import serializers

from apps.common.serializers import TranslatedJSONField
from apps.pages.models import SiteSettings


class SiteSettingsAdminSerializer(serializers.ModelSerializer):
    address = TranslatedJSONField(required=False)
    work_hours = TranslatedJSONField(required=False)
    cookie_notice_text = TranslatedJSONField(required=False)

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
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")
