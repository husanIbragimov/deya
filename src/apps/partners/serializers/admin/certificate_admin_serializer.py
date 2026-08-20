from rest_framework import serializers

from apps.common.serializers import TranslatedJSONField
from apps.partners.models import Certificate


class CertificateAdminSerializer(serializers.ModelSerializer):
    title = TranslatedJSONField()

    class Meta:
        model = Certificate
        fields = ("id", "title", "image", "file", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
