from rest_framework import serializers

from apps.common.serializers import TranslatedField
from apps.pages.models import StaticPage


class StaticPageSerializer(serializers.ModelSerializer):
    title = TranslatedField()
    body = TranslatedField()

    class Meta:
        model = StaticPage
        fields = ("id", "slug", "title", "body")
