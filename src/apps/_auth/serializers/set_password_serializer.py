from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)

    def validate_password(self, value):
        validate_password(value)
        return value
