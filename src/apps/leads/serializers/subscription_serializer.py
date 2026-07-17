from rest_framework import serializers


class SubscriptionCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UnsubscribeResultSerializer(serializers.Serializer):
    email = serializers.EmailField()
    is_active = serializers.BooleanField()
