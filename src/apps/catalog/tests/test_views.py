from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.catalog.models import Category, Flavor, Product, ProductFamily, Weight
from apps.catalog.tests.helpers import tr


def make_product(category, name, **kwargs):
    defaults = dict(box_weight="1.500", shelf_life_months=6, is_active=True)
    defaults.update(kwargs)
    return Product.objects.create(category=category, name=tr(name), **defaults)


class CategoryListViewTests(APITestCase):
    def test_only_active_categories_are_listed(self):
        Category.objects.create(
            name={"ru": "Круассаны", "en": "Croissants"}, slug="croissants", image="c.jpg", is_active=True
        )
        Category.objects.create(name=tr("Архив"), slug="archive", image="a.jpg", is_active=False)

        response = self.client.get(reverse("catalog:category-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["slug"], "croissants")

    def test_name_follows_accept_language_header(self):
        Category.objects.create(
            name={"ru": "Круассаны", "en": "Croissants"}, slug="croissants", image="c.jpg", is_active=True
        )

        response_ru = self.client.get(reverse("catalog:category-list"), HTTP_ACCEPT_LANGUAGE="ru")
        response_en = self.client.get(reverse("catalog:category-list"), HTTP_ACCEPT_LANGUAGE="en")

        self.assertEqual(response_ru.data[0]["name"], "Круассаны")
        self.assertEqual(response_en.data[0]["name"], "Croissants")


class ProductListViewTests(APITestCase):
    def setUp(self):
        self.category_a = Category.objects.create(name=tr("Круассаны"), slug="croissants", image="c.jpg")
        self.category_b = Category.objects.create(name=tr("Вафли"), slug="waffles", image="w.jpg")
        self.product_a = make_product(self.category_a, "Ketler", slug="ketler", code="A1")
        self.product_b = make_product(self.category_b, "Taggis", slug="taggis", code="B1")

    def test_filters_by_category(self):
        response = self.client.get(reverse("catalog:product-list"), {"category": self.category_a.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        slugs = [item["slug"] for item in response.data["results"]]
        self.assertEqual(slugs, ["ketler"])

    def test_search_filters_by_name(self):
        response = self.client.get(reverse("catalog:product-list"), {"search": "Taggis"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        slugs = [item["slug"] for item in response.data["results"]]
        self.assertEqual(slugs, ["taggis"])

    def test_is_paginated(self):
        response = self.client.get(reverse("catalog:product-list"))

        self.assertIn("results", response.data)
        self.assertIn("count", response.data)


class ProductDetailViewTests(APITestCase):
    def test_detail_includes_family_variants(self):
        category = Category.objects.create(name=tr("Круассаны"), slug="croissants", image="c.jpg")
        family = ProductFamily.objects.create(name="Ketler", slug="ketler")
        product = make_product(category, "Ketler choco", family=family, slug="ketler-choco", code="A1")
        make_product(category, "Ketler raspberry", family=family, slug="ketler-raspberry", code="A2")

        response = self.client.get(reverse("catalog:product-detail", kwargs={"slug": product.slug}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["variants"]), 1)
        self.assertEqual(response.data["variants"][0]["slug"], "ketler-raspberry")

    def test_detail_variants_include_flavor_and_weight(self):
        category = Category.objects.create(name=tr("Круассаны"), slug="croissants", image="c.jpg")
        family = ProductFamily.objects.create(name="Ketler", slug="ketler")
        small = Weight.objects.create(value="45.00", unit="g")
        large = Weight.objects.create(value="90.00", unit="g")
        product = make_product(category, "Ketler 45g", family=family, weight=small, slug="ketler-45", code="W1")
        make_product(category, "Ketler 90g", family=family, weight=large, slug="ketler-90", code="W2")

        response = self.client.get(reverse("catalog:product-detail", kwargs={"slug": product.slug}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["weight"], {"id": small.id, "value": "45.00", "unit": "g"})
        variant = response.data["variants"][0]
        self.assertEqual(variant["slug"], "ketler-90")
        self.assertEqual(variant["weight"], {"id": large.id, "value": "90.00", "unit": "g"})
        self.assertIn("flavor", variant)

    def test_variants_are_ordered_by_flavor_then_weight(self):
        category = Category.objects.create(name=tr("Круассаны"), slug="croissants", image="c.jpg")
        family = ProductFamily.objects.create(name="Ketler", slug="ketler")
        choco = Flavor.objects.create(name=tr("Шоколад"), slug="choco", sort_order=1)
        berry = Flavor.objects.create(name=tr("Малина"), slug="berry", sort_order=2)
        small = Weight.objects.create(value="45.00", unit="g")
        large = Weight.objects.create(value="90.00", unit="g")
        current = make_product(category, "c45", family=family, flavor=choco, weight=small, slug="c45", code="V1")
        make_product(category, "b90", family=family, flavor=berry, weight=large, slug="b90", code="V2")
        make_product(category, "b45", family=family, flavor=berry, weight=small, slug="b45", code="V3")
        make_product(category, "c90", family=family, flavor=choco, weight=large, slug="c90", code="V4")

        response = self.client.get(reverse("catalog:product-detail", kwargs={"slug": current.slug}))

        self.assertEqual([v["slug"] for v in response.data["variants"]], ["c90", "b45", "b90"])

    def test_list_filters_by_weight(self):
        category = Category.objects.create(name=tr("Круассаны"), slug="croissants", image="c.jpg")
        small = Weight.objects.create(value="45.00", unit="g")
        large = Weight.objects.create(value="90.00", unit="g")
        make_product(category, "a", weight=small, slug="a", code="F1")
        make_product(category, "b", weight=large, slug="b", code="F2")

        response = self.client.get(reverse("catalog:product-list"), {"weight": large.pk})

        self.assertEqual([item["slug"] for item in response.data["results"]], ["b"])


class ProductRelatedViewTests(APITestCase):
    def test_falls_back_to_same_category(self):
        category = Category.objects.create(name=tr("Печенье"), slug="cookies", image="c.jpg")
        product = make_product(category, "Quadro", slug="quadro", code="D1")
        sibling = make_product(category, "Quadro 2", slug="quadro-2", code="D2")

        response = self.client.get(reverse("catalog:product-related", kwargs={"slug": product.slug}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["slug"] for item in response.data], [sibling.slug])
