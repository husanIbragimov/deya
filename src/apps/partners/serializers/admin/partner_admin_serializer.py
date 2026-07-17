from rest_framework import serializers

from apps.partners.models import Partner


class PartnerAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ("id", "name", "logo", "website", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
