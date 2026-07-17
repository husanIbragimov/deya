from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.pages.models import SiteSettings, StaticPage


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
