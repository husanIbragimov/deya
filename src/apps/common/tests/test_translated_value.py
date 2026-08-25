from django.test import SimpleTestCase

from apps.common.utils.translated_value import translated_value


class TranslatedValueTests(SimpleTestCase):
    def test_empty_dict_returns_empty_string(self):
        self.assertEqual(translated_value({}), "")

    def test_none_returns_empty_string(self):
        self.assertEqual(translated_value(None), "")

    def test_returns_active_language_code_value(self):
        self.assertEqual(translated_value({"ru": "Привет", "en": "Hello"}), "Привет")

    def test_falls_back_to_any_available_value(self):
        self.assertEqual(translated_value({"en": "Hello"}), "Hello")

    def test_legacy_plain_string_is_returned_unchanged(self):
        self.assertEqual(translated_value("Legacy name"), "Legacy name")
