from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.pages.models import Banner, PrivacyPolicy, SiteSettings, StaticPage


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
    def test_list_returns_all_records(self):
        PrivacyPolicy.objects.create(slug="for-users", title={"uz": "a", "ru": "a", "en": "a"})
        PrivacyPolicy.objects.create(slug="for-partners", title={"uz": "b", "ru": "b", "en": "b"})

        response = self.client.get(reverse("pages:privacy-policy-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_detail_returns_full_multilingual_object_by_slug(self):
        PrivacyPolicy.objects.create(
            slug="for-users",
            title={"uz": "Maxfiylik siyosati", "ru": "Политика конфиденциальности", "en": "Privacy Policy"},
            body={"uz": "Matn", "ru": "Текст", "en": "Text"},
        )

        response = self.client.get(reverse("pages:privacy-policy-detail", kwargs={"slug": "for-users"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["title"],
            {"uz": "Maxfiylik siyosati", "ru": "Политика конфиденциальности", "en": "Privacy Policy"},
        )
        self.assertEqual(response.data["body"], {"uz": "Matn", "ru": "Текст", "en": "Text"})

    def test_detail_returns_404_for_unknown_slug(self):
        response = self.client.get(reverse("pages:privacy-policy-detail", kwargs={"slug": "missing"}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BannerListViewTests(APITestCase):
    def test_filters_by_type(self):
        Banner.objects.create(type="partner", title={"ru": "a", "en": "a"}, image="banners/partner.png")
        Banner.objects.create(type="partner", title={"ru": "b", "en": "b"}, image="banners/partner2.png")

        response = self.client.get(reverse("pages:banner-list"), {"type": "partner"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(all(item["type"] == "partner" for item in response.data))

    def test_unfiltered_returns_all_banners(self):
        Banner.objects.create(type="partner", title={"ru": "a", "en": "a"}, image="banners/partner.png")

        response = self.client.get(reverse("pages:banner-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unknown_type_returns_empty_list(self):
        Banner.objects.create(type="partner", title={"ru": "a", "en": "a"}, image="banners/partner.png")

        response = self.client.get(reverse("pages:banner-list"), {"type": "unknown"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
