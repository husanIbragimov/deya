from rest_framework import serializers

from apps.about.models import HomeSlide


class HomeSlideAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeSlide
        fields = ("id", "title", "subtitle", "image", "cta_label", "cta_url", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
