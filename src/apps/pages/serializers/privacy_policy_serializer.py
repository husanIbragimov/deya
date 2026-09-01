from rest_framework import serializers

from apps.pages.models import PrivacyPolicy


class PrivacyPolicySerializer(serializers.ModelSerializer):
    """Returns title/body as the full {"uz": ..., "ru": ..., "en": ...} object.

    Unlike other public serializers, the frontend picks the language itself here
    instead of the backend resolving one via TranslatedField, since "uz" isn't
    among settings.LANGUAGES and so can never be the active Django language.
    """

    class Meta:
        model = PrivacyPolicy
        fields = ("slug", "title", "body")
