from rest_framework import serializers

from apps.leads.models import Lead


class LeadAdminSerializer(serializers.ModelSerializer):
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
            "status",
            "source_url",
            "ip_address",
            "user_agent",
            "created_at",
        )
        read_only_fields = fields


class LeadStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ("status",)
