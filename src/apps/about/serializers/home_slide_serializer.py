from rest_framework import serializers

from apps.about.models import HomeSlide
from apps.common.serializers import TranslatedField


class HomeSlideSerializer(serializers.ModelSerializer):
    title = TranslatedField()
    subtitle = TranslatedField()
    cta_label = TranslatedField()

    class Meta:
        model = HomeSlide
        fields = ("id", "title", "subtitle", "image", "cta_label", "cta_url")
