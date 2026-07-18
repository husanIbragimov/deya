from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps._auth.models import User


class UserAdminCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, allow_blank=False, max_length=150)
    last_name = serializers.CharField(required=True, allow_blank=False, max_length=150)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "password", "role", "date_joined"]
        read_only_fields = ["id", "date_joined"]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)
