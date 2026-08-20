from rest_framework import serializers

from apps.common.serializers import TranslatedJSONField
from apps.pages.models import StaticPage


class StaticPageAdminSerializer(serializers.ModelSerializer):
    title = TranslatedJSONField()
    body = TranslatedJSONField(required=False)

    class Meta:
        model = StaticPage
        fields = ("id", "slug", "title", "body", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
