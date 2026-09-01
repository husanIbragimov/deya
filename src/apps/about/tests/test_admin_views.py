from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps._auth.models import User
from apps.about.models import Factory, ProductInfo, Stat


class StatAdminCrudTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)

    def test_create_and_delete_flow(self):
        create_response = self.client.post(
            reverse("about-admin:stat-admin-list"),
            data={"value": "32+", "label": {"ru": "стран", "en": "countries"}},
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED, create_response.data)
        stat_id = create_response.data["id"]

        delete_response = self.client.delete(reverse("about-admin:stat-admin-detail", kwargs={"pk": stat_id}))
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Stat.objects.filter(pk=stat_id).exists())


class FactoryAdminViewTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="factory-admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)

    def test_get_creates_default_singleton(self):
        response = self.client.get(reverse("about-admin:factory-admin"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Factory.objects.count(), 1)

    def test_put_updates_singleton_in_place(self):
        Factory.objects.create(title={"ru": "Старый", "en": "Old"}, image="old.jpg")

        response = self.client.put(
            reverse("about-admin:factory-admin"),
            data={
                "title": {"ru": "Завод", "en": "Factory"},
                "subtitle": {"ru": "Подзаголовок", "en": "Subtitle"},
                "description": {"ru": "Описание", "en": "Description"},
                "subdescription": {"ru": "Доп. описание", "en": "Subdescription"},
                "image": "factory-banner.jpg",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(Factory.objects.count(), 1)
        self.assertEqual(Factory.objects.get().image, "factory-banner.jpg")

    def test_non_admin_forbidden(self):
        self.client.force_authenticate(User.objects.create_user(username="visitor2", password="pass12345"))
        response = self.client.get(reverse("about-admin:factory-admin"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_creates_singleton_when_missing(self):
        response = self.client.post(
            reverse("about-admin:factory-admin"),
            data={
                "title": {"ru": "Завод", "en": "Factory"},
                "image": "factory-banner.jpg",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Factory.objects.count(), 1)
        self.assertEqual(Factory.objects.get().image, "factory-banner.jpg")

    def test_post_rejects_when_already_exists(self):
        Factory.objects.create(title={"ru": "Старый", "en": "Old"}, image="old.jpg")

        response = self.client.post(
            reverse("about-admin:factory-admin"),
            data={"title": {"ru": "Завод", "en": "Factory"}, "image": "new.jpg"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(Factory.objects.count(), 1)
        self.assertEqual(Factory.objects.get().image, "old.jpg")


class ProductInfoAdminCrudTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="product-info-admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)

    def test_create_list_update_delete_flow(self):
        create_response = self.client.post(
            reverse("about-admin:product-info-admin-list"),
            data={
                "title": {"ru": "Круассан", "en": "Croissant"},
                "description": {"ru": "Описание", "en": "Description"},
                "image": "product.jpg",
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED, create_response.data)
        product_info_id = create_response.data["id"]

        list_response = self.client.get(reverse("about-admin:product-info-admin-list"))
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)

        update_response = self.client.put(
            reverse("about-admin:product-info-admin-detail", kwargs={"pk": product_info_id}),
            data={
                "title": {"ru": "Круассан New", "en": "Croissant New"},
                "image": "product-new.jpg",
            },
            format="json",
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK, update_response.data)
        self.assertEqual(ProductInfo.objects.get(pk=product_info_id).image, "product-new.jpg")

        delete_response = self.client.delete(
            reverse("about-admin:product-info-admin-detail", kwargs={"pk": product_info_id})
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ProductInfo.objects.filter(pk=product_info_id).exists())

    def test_non_admin_forbidden(self):
        self.client.force_authenticate(User.objects.create_user(username="visitor4", password="pass12345"))
        response = self.client.get(reverse("about-admin:product-info-admin-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
