from django.conf import settings
from django.utils.translation import get_language
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _

TRANSLATED_JSON_LANGUAGES = ("ru", "en")


@extend_schema_field(OpenApiTypes.OBJECT)
class TranslatedJSONField(serializers.JSONField):
    """Validates a {"ru": "...", "en": "..."} JSONField value.

    Rejects anything that isn't a dict keyed by exactly `languages` (defaults to
    TRANSLATED_JSON_LANGUAGES) with string values. Pass `languages=(...)` to require a
    different set for a specific field (e.g. legal pages that need "uz" too).
    """

    default_error_messages = {
        "not_a_dict": _(T.translated_json_not_a_dict),
        "invalid_keys": _(T.translated_json_invalid_keys),
        "invalid_value": _(T.translated_json_invalid_value),
    }

    def __init__(self, *, languages=TRANSLATED_JSON_LANGUAGES, **kwargs):
        self.languages = languages
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        if not isinstance(value, dict):
            self.fail("not_a_dict")
        if set(value.keys()) != set(self.languages):
            self.fail("invalid_keys", languages=", ".join(self.languages))
        for lang, text in value.items():
            if not isinstance(text, str):
                self.fail("invalid_value", lang=lang)
        return value


@extend_schema_field(OpenApiTypes.STR)
class TranslatedField(serializers.Field):
    """Renders a {"ru": "...", "en": "..."} JSONField as a single string in the active language.

    Falls back to settings.LANGUAGE_CODE, then to any available value, so a missing
    translation doesn't blank out the response. Legacy plain-string values are
    returned unchanged.
    """

    def __init__(self, **kwargs):
        kwargs["read_only"] = True
        super().__init__(**kwargs)

    @staticmethod
    def to_representation(value: dict[str, str] | str) -> str:
        if not value:
            return ""
        if isinstance(value, str):
            return value
        lang = get_language() or settings.LANGUAGE_CODE
        text = value.get(lang) or value.get(settings.LANGUAGE_CODE)
        if text:
            return text
        return next(iter(value.values()), "")
