from rest_framework import serializers

from apps.common.serializers import TranslatedField
from apps.pages.models import Banner


class BannerSerializer(serializers.ModelSerializer):
    title = TranslatedField()
    subtitle = TranslatedField()
    cta_label = TranslatedField()

    class Meta:
        model = Banner
        fields = ("id", "type", "title", "subtitle", "image", "cta_label", "cta_url")
