from rest_framework import serializers

from apps.careers.models import Company


class CompanyAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name", "slug", "description", "image", "vacancies_url", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
