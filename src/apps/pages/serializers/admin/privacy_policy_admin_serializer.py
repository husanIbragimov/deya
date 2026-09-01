from rest_framework import serializers

from apps.common.serializers import TranslatedJSONField
from apps.pages.models import PrivacyPolicy

PRIVACY_POLICY_LANGUAGES = ("uz", "ru", "en")


class PrivacyPolicyAdminSerializer(serializers.ModelSerializer):
    title = TranslatedJSONField(languages=PRIVACY_POLICY_LANGUAGES)
    body = TranslatedJSONField(languages=PRIVACY_POLICY_LANGUAGES, required=False)

    class Meta:
        model = PrivacyPolicy
        fields = ("slug", "title", "body", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")
