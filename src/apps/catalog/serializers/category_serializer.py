from rest_framework import serializers

from apps.catalog.models import Category
from apps.common.serializers import TranslatedField


class CategorySerializer(serializers.ModelSerializer):
    name = TranslatedField()

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "image", "sort_order")
