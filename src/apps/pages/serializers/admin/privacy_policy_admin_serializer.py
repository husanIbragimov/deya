from rest_framework import serializers

from apps.common.serializers import TranslatedJSONField
from apps.pages.models import PrivacyPolicy


class PrivacyPolicyAdminSerializer(serializers.ModelSerializer):
    title = TranslatedJSONField()
    body = TranslatedJSONField(required=False)

    class Meta:
        model = PrivacyPolicy
        fields = ("slug", "title", "body", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")
