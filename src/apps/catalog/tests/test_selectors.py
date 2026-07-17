from django.test import TestCase

from apps.catalog.models import Category, Product, ProductFamily
from apps.catalog.selectors import get_family_variants, get_related_products
from apps.catalog.tests.helpers import tr


def make_product(category, name, **kwargs):
    defaults = dict(box_weight="1.500", shelf_life_months=6)
    defaults.update(kwargs)
    return Product.objects.create(category=category, name=tr(name), **defaults)


class GetFamilyVariantsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name=tr("Круассаны"), slug="croissants", image="c.jpg")
        self.family = ProductFamily.objects.create(name="Ketler", slug="ketler")

    def test_returns_other_active_products_in_same_family(self):
        product = make_product(self.category, "Ketler choco", family=self.family, slug="ketler-choco", code="A1")
        sibling = make_product(
            self.category, "Ketler raspberry", family=self.family, slug="ketler-raspberry", code="A2"
        )
        variants = list(get_family_variants(product))
        self.assertEqual(variants, [sibling])

    def test_no_family_returns_empty(self):
        product = make_product(self.category, "Solo", slug="solo", code="B1")
        self.assertEqual(list(get_family_variants(product)), [])


class GetRelatedProductsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name=tr("Вафли"), slug="waffles", image="w.jpg")

    def test_uses_explicit_related_products_when_set(self):
        product = make_product(self.category, "Taggis", slug="taggis", code="C1")
        other_category = Category.objects.create(name=tr("Конфеты"), slug="candies", image="k.jpg")
        explicit_related = make_product(other_category, "Apachi", slug="apachi", code="C2")
        product.related_products.add(explicit_related)

        related = list(get_related_products(product))
        self.assertEqual(related, [explicit_related])

    def test_falls_back_to_same_category_when_empty(self):
        product = make_product(self.category, "Quadro", slug="quadro", code="D1")
        same_category_product = make_product(self.category, "Quadro 2", slug="quadro-2", code="D2")

        related = list(get_related_products(product))
        self.assertEqual(related, [same_category_product])
