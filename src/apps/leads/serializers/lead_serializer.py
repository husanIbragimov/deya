from rest_framework import serializers

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.leads.models import Lead


class LeadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = (
            "id",
            "type",
            "name",
            "email",
            "phone",
            "message",
            "product",
            "consent_personal_data",
            "consent_marketing",
        )
        read_only_fields = ("id",)

    def validate_consent_personal_data(self, value: bool) -> bool:
        if not value:
            raise serializers.ValidationError(str(_(T.consent_personal_data_required)))
        return value
