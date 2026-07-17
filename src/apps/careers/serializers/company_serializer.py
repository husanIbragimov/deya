from rest_framework import serializers

from apps.careers.models import Company
from apps.common.serializers import TranslatedField


class CompanySerializer(serializers.ModelSerializer):
    description = TranslatedField()

    class Meta:
        model = Company
        fields = ("id", "name", "slug", "description", "image", "vacancies_url")
