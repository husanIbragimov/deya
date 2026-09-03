from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps._auth.models import User
from apps.pages.models import Banner, PrivacyPolicy, SiteSettings


class SiteSettingsAdminViewTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)

    def test_get_creates_default_singleton(self):
        response = self.client.get(reverse("pages-admin:site-settings-admin"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_updates_singleton_in_place(self):
        SiteSettings.objects.create(phone="+998901234567", email="old@example.com")

        response = self.client.put(
            reverse("pages-admin:site-settings-admin"),
            data={"phone": "+998901234567", "email": "new@example.com"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(SiteSettings.objects.count(), 1)
        self.assertEqual(SiteSettings.objects.get().email, "new@example.com")

    def test_non_admin_forbidden(self):
        self.client.force_authenticate(User.objects.create_user(username="visitor", password="pass12345"))
        response = self.client.get(reverse("pages-admin:site-settings-admin"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PrivacyPolicyAdminViewTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="privacy-admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)

    def test_put_requires_all_three_languages(self):
        PrivacyPolicy.objects.create(slug="for-users", title={"uz": "a", "ru": "a", "en": "a"})

        response = self.client.put(
            reverse("pages-admin:privacy-policy-admin-detail", kwargs={"slug": "for-users"}),
            data={"title": {"ru": "Политика", "en": "Policy"}},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("uz, ru, en", str(response.data["title"][0]))

    def test_create_list_update_delete_flow(self):
        create_response = self.client.post(
            reverse("pages-admin:privacy-policy-admin-list"),
            data={
                "slug": "for-users",
                "title": {"uz": "Maxfiylik siyosati", "ru": "Политика конфиденциальности", "en": "Privacy Policy"},
                "body": {"uz": "Matn", "ru": "Текст", "en": "Text"},
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED, create_response.data)

        list_response = self.client.get(reverse("pages-admin:privacy-policy-admin-list"))
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)

        update_response = self.client.put(
            reverse("pages-admin:privacy-policy-admin-detail", kwargs={"slug": "for-users"}),
            data={
                "slug": "for-users",
                "title": {"uz": "Yangilangan", "ru": "Обновлено", "en": "Updated"},
                "body": {"uz": "Matn", "ru": "Текст", "en": "Text"},
            },
            format="json",
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK, update_response.data)
        self.assertEqual(PrivacyPolicy.objects.get(slug="for-users").title["uz"], "Yangilangan")

        delete_response = self.client.delete(
            reverse("pages-admin:privacy-policy-admin-detail", kwargs={"slug": "for-users"})
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PrivacyPolicy.objects.filter(slug="for-users").exists())

    def test_post_allows_more_than_one_record(self):
        PrivacyPolicy.objects.create(slug="for-users", title={"uz": "a", "ru": "a", "en": "a"})

        response = self.client.post(
            reverse("pages-admin:privacy-policy-admin-list"),
            data={"slug": "for-partners", "title": {"uz": "b", "ru": "b", "en": "b"}},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(PrivacyPolicy.objects.count(), 2)

    def test_non_admin_forbidden(self):
        self.client.force_authenticate(User.objects.create_user(username="visitor3", password="pass12345"))
        response = self.client.get(reverse("pages-admin:privacy-policy-admin-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class BannerAdminViewTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="banner-admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)

    def test_create_list_update_delete_flow(self):
        create_response = self.client.post(
            reverse("pages-admin:banner-admin-list"),
            data={
                "type": "partner",
                "title": {"uz": "Banner", "ru": "Баннер", "en": "Banner"},
                "image": "banners/partner.png",
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED, create_response.data)
        banner_id = create_response.data["id"]

        list_response = self.client.get(reverse("pages-admin:banner-admin-list"))
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)

        update_response = self.client.put(
            reverse("pages-admin:banner-admin-detail", kwargs={"pk": banner_id}),
            data={
                "type": "partner",
                "title": {"uz": "Yangilangan", "ru": "Обновлено", "en": "Updated"},
                "image": "banners/partner-updated.png",
            },
            format="json",
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK, update_response.data)
        self.assertEqual(Banner.objects.get(pk=banner_id).title["en"], "Updated")

        delete_response = self.client.delete(reverse("pages-admin:banner-admin-detail", kwargs={"pk": banner_id}))
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Banner.objects.filter(pk=banner_id).exists())

    def test_create_rejects_invalid_type(self):
        response = self.client.post(
            reverse("pages-admin:banner-admin-list"),
            data={"type": "unknown", "title": {"ru": "a", "en": "a"}, "image": "banners/a.png"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_non_admin_forbidden(self):
        self.client.force_authenticate(User.objects.create_user(username="visitor4", password="pass12345"))
        response = self.client.get(reverse("pages-admin:banner-admin-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
