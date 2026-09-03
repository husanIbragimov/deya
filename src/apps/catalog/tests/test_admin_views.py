import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps._auth.models import User
from apps.catalog.models import Category


class CategoryAdminPermissionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="visitor", password="pass12345")
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)

    def test_anonymous_cannot_list(self):
        response = self.client.get(reverse("catalog-admin:category-admin-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_admin_cannot_create(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse("catalog-admin:category-admin-list"), data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CategoryAdminCrudTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)

    def test_create_list_update_delete_flow(self):
        create_response = self.client.post(
            reverse("catalog-admin:category-admin-list"),
            data={
                "name": json.dumps({"uz": "Kruassanlar", "ru": "Круассаны", "en": "Croissants"}),
                "slug": "croissants",
                "image": "croissants.jpg",
                "sort_order": 1,
            },
            format="multipart",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED, create_response.data)
        category_id = create_response.data["id"]

        list_response = self.client.get(reverse("catalog-admin:category-admin-list"))
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)

        detail_url = reverse("catalog-admin:category-admin-detail", kwargs={"pk": category_id})

        # updating without changing the unique slug must not self-conflict
        update_response = self.client.put(
            detail_url,
            data={
                "name": json.dumps({"uz": "Kruassanlar yangi", "ru": "Круассаны новый", "en": "Croissants new"}),
                "slug": "croissants",
                "image": "croissants-new.jpg",
                "sort_order": 2,
            },
            format="multipart",
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK, update_response.data)
        self.assertEqual(update_response.data["name"]["ru"], "Круассаны новый")

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(pk=category_id).exists())
