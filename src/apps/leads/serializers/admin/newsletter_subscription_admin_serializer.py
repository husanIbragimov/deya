from rest_framework import serializers

from apps.leads.models import NewsletterSubscription


class NewsletterSubscriptionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscription
        fields = ("id", "email", "is_active", "unsubscribe_token", "created_at")
        read_only_fields = fields
