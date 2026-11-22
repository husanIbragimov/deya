import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps._auth.models import User
from apps.catalog.models import Category, Flavor, ProductFamily, Weight


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


class ProductAdminTestBase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)
        self.category = Category.objects.create(name={"ru": "Круассаны"}, slug="croissants", image="c.jpg")
        self.family = ProductFamily.objects.create(name="Ketler", slug="ketler")
        self.flavor = Flavor.objects.create(name={"ru": "Шоколад"}, slug="choco")
        self.small = Weight.objects.create(value="45.00", unit="g")
        self.large = Weight.objects.create(value="90.00", unit="g")

    def _payload(self, code, weight):
        return {
            "category": self.category.pk,
            "family": self.family.pk,
            "flavor": self.flavor.pk,
            "weight": weight.pk,
            "name": {"uz": code, "ru": code, "en": code},
            "slug": code.lower(),
            "code": code,
            "box_weight": "1.500",
            "shelf_life_months": 6,
        }


class ProductVariantAdminTests(ProductAdminTestBase):
    def test_same_flavor_different_weights_are_separate_variants(self):
        url = reverse("catalog-admin:product-admin-list")

        first = self.client.post(url, data=self._payload("K45", self.small), format="json")
        second = self.client.post(url, data=self._payload("K90", self.large), format="json")

        self.assertEqual(first.status_code, status.HTTP_201_CREATED, first.data)
        self.assertEqual(second.status_code, status.HTTP_201_CREATED, second.data)
        self.assertEqual(second.data["weight"], self.large.pk)

    def test_duplicate_flavor_and_weight_in_family_is_rejected(self):
        url = reverse("catalog-admin:product-admin-list")
        self.client.post(url, data=self._payload("K45", self.small), format="json")

        response = self.client.post(url, data=self._payload("K45B", self.small), format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)

    def test_update_keeping_own_flavor_and_weight_is_allowed(self):
        url = reverse("catalog-admin:product-admin-list")
        created = self.client.post(url, data=self._payload("K45", self.small), format="json")

        response = self.client.patch(
            reverse("catalog-admin:product-admin-detail", kwargs={"pk": created.data["id"]}),
            data={"weight": self.small.pk, "sort_order": 3},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

    def test_patch_to_taken_weight_is_rejected(self):
        url = reverse("catalog-admin:product-admin-list")
        self.client.post(url, data=self._payload("K45", self.small), format="json")
        other = self.client.post(url, data=self._payload("K90", self.large), format="json")

        response = self.client.patch(
            reverse("catalog-admin:product-admin-detail", kwargs={"pk": other.data["id"]}),
            data={"weight": self.small.pk},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)


class BoxQuantityAdminTests(ProductAdminTestBase):
    def test_product_create_saves_box_quantity(self):
        payload = {**self._payload("K45", self.small), "box_quantity": "24", "box_quantity_unit": "pcs"}

        response = self.client.post(reverse("catalog-admin:product-admin-list"), data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data["box_quantity"], "24.000")
        self.assertEqual(response.data["box_quantity_unit"], "pcs")

    def test_product_box_quantity_without_unit_is_rejected(self):
        payload = {**self._payload("K45", self.small), "box_quantity": "5.5"}

        response = self.client.post(reverse("catalog-admin:product-admin-list"), data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)

    def test_product_unit_without_box_quantity_is_rejected(self):
        payload = {**self._payload("K45", self.small), "box_quantity_unit": "kg"}

        response = self.client.post(reverse("catalog-admin:product-admin-list"), data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)

    def test_family_create_saves_box_quantity(self):
        response = self.client.post(
            reverse("catalog-admin:product-family-admin-list"),
            data={"name": "Choco", "slug": "choco", "box_quantity": "5.5", "box_quantity_unit": "kg"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data["box_quantity"], "5.500")
        self.assertEqual(response.data["box_quantity_unit"], "kg")

    def test_family_patch_clearing_only_quantity_is_rejected(self):
        self.family.box_quantity, self.family.box_quantity_unit = "12", "pcs"
        self.family.save()

        response = self.client.patch(
            reverse("catalog-admin:product-family-admin-detail", kwargs={"pk": self.family.pk}),
            data={"box_quantity": None},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
