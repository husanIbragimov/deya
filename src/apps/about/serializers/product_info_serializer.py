from rest_framework import serializers

from apps.about.models import ProductInfo
from apps.common.serializers import TranslatedField


class ProductInfoSerializer(serializers.ModelSerializer):
    title = TranslatedField()
    description = TranslatedField()

    class Meta:
        model = ProductInfo
        fields = ("id", "title", "description", "image")
