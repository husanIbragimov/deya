from django.test import SimpleTestCase
from rest_framework import serializers

from apps.common.serializers import TranslatedJSONField


class _Instance:
    def __init__(self, title):
        self.title = title


class _Serializer(serializers.Serializer):
    title = TranslatedJSONField()


class TranslatedJSONFieldTests(SimpleTestCase):
    def test_full_payload_is_accepted(self):
        serializer = _Serializer(data={"title": {"uz": "Sarlavha", "ru": "Заголовок", "en": "Title"}})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["title"], {"uz": "Sarlavha", "ru": "Заголовок", "en": "Title"})

    def test_unknown_language_key_is_rejected(self):
        serializer = _Serializer(data={"title": {"uz": "a", "ru": "b", "en": "c", "fr": "d"}})
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_non_string_value_is_rejected(self):
        serializer = _Serializer(data={"title": {"uz": "a", "ru": "b", "en": 1}})
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_partial_payload_on_create_is_rejected(self):
        """POST is a full write (no partial=True), so it keeps requiring every language."""
        serializer = _Serializer(data={"title": {"uz": "Sarlavha"}})
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_partial_payload_on_full_update_is_rejected(self):
        """PUT (partial=False) is a full replacement, so a partial locale payload must still fail."""
        instance = _Instance(title={"uz": "Sarlavha", "ru": "Заголовок", "en": "Title"})
        serializer = _Serializer(instance, data={"title": {"uz": "Yangilangan"}})
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_partial_payload_on_patch_merges_with_existing_instance(self):
        """PATCH from the admin editing only the active locale tab must not wipe other locales."""
        instance = _Instance(title={"uz": "Sarlavha", "ru": "Заголовок", "en": "Title"})
        serializer = _Serializer(instance, data={"title": {"uz": "Yangilangan"}}, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(
            serializer.validated_data["title"],
            {"uz": "Yangilangan", "ru": "Заголовок", "en": "Title"},
        )
