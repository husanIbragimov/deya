from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.pages.models import PrivacyPolicy, SiteSettings, StaticPage


class StaticPageModelTests(TestCase):
    def test_slug_is_unique(self):
        StaticPage.objects.create(slug="privacy-policy", title={"ru": "a", "en": "a"})
        with self.assertRaises(IntegrityError), transaction.atomic():
            StaticPage.objects.create(slug="privacy-policy", title={"ru": "b", "en": "b"})


class PrivacyPolicyModelTests(TestCase):
    def test_slug_is_unique(self):
        PrivacyPolicy.objects.create(slug="for-users", title={"ru": "a", "en": "a"})
        with self.assertRaises(IntegrityError), transaction.atomic():
            PrivacyPolicy.objects.create(slug="for-users", title={"ru": "b", "en": "b"})

    def test_allows_more_than_one_record(self):
        PrivacyPolicy.objects.create(slug="for-users", title={"ru": "a", "en": "a"})
        PrivacyPolicy.objects.create(slug="for-partners", title={"ru": "b", "en": "b"})

        self.assertEqual(PrivacyPolicy.objects.count(), 2)


class SiteSettingsModelTests(TestCase):
    def test_save_always_writes_to_pk_one(self):
        first = SiteSettings.objects.create(phone="+998901234567", email="a@example.com")

        loaded = SiteSettings.load()
        loaded.phone = "+998901234568"
        loaded.save()

        self.assertEqual(first.pk, 1)
        self.assertEqual(loaded.pk, 1)
        self.assertEqual(SiteSettings.objects.count(), 1)
        self.assertEqual(SiteSettings.objects.get().phone, "+998901234568")

    def test_load_creates_if_missing(self):
        self.assertEqual(SiteSettings.objects.count(), 0)
        instance = SiteSettings.load()
        self.assertEqual(instance.pk, 1)
        self.assertEqual(SiteSettings.objects.count(), 1)
