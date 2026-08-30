from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.pages.models import PrivacyPolicy, SiteSettings, StaticPage


class SiteSettingsViewTests(APITestCase):
    def test_returns_singleton_even_when_unconfigured(self):
        response = self.client.get(reverse("pages:site-settings"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SiteSettings.objects.count(), 1)

    def test_returns_configured_values(self):
        SiteSettings.objects.create(phone="+998901234567", email="info@example.com")

        response = self.client.get(reverse("pages:site-settings"))

        self.assertEqual(response.data["phone"], "+998901234567")


class StaticPageDetailViewTests(APITestCase):
    def test_returns_page_by_slug(self):
        StaticPage.objects.create(slug="privacy-policy", title={"ru": "Политика", "en": "Policy"})

        response = self.client.get(reverse("pages:static-page-detail", kwargs={"slug": "privacy-policy"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Политика")


class PrivacyPolicyViewTests(APITestCase):
    def test_returns_singleton_even_when_unconfigured(self):
        response = self.client.get(reverse("pages:privacy-policy"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PrivacyPolicy.objects.count(), 1)

    def test_returns_full_multilingual_object(self):
        PrivacyPolicy.objects.create(
            title={"uz": "Maxfiylik siyosati", "ru": "Политика конфиденциальности", "en": "Privacy Policy"},
            body={"uz": "Matn", "ru": "Текст", "en": "Text"},
        )

        response = self.client.get(reverse("pages:privacy-policy"))

        self.assertEqual(
            response.data["title"],
            {"uz": "Maxfiylik siyosati", "ru": "Политика конфиденциальности", "en": "Privacy Policy"},
        )
        self.assertEqual(response.data["body"], {"uz": "Matn", "ru": "Текст", "en": "Text"})
