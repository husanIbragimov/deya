from rest_framework import serializers

from apps.common.serializers import TranslatedField
from apps.partners.models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    title = TranslatedField()

    class Meta:
        model = Certificate
        fields = ("id", "title", "image", "file")
