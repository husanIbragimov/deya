from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.catalog.choices import WeightUnitChoice
from apps.catalog.models import Category, Product, Weight
from apps.catalog.tests.helpers import tr


class WeightModelTests(TestCase):
    def test_duplicate_value_and_unit_is_rejected(self):
        Weight.objects.create(value="42.00", unit=WeightUnitChoice.GRAM)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Weight.objects.create(value="42.00", unit=WeightUnitChoice.GRAM)

    def test_same_value_different_unit_is_allowed(self):
        Weight.objects.create(value="42.00", unit=WeightUnitChoice.GRAM)
        Weight.objects.create(value="42.00", unit=WeightUnitChoice.KILOGRAM)
        self.assertEqual(Weight.objects.count(), 2)


class ProductModelTests(TestCase):
    def test_code_is_unique(self):
        category = Category.objects.create(name=tr("Круассаны"), slug="croissants", image="c.jpg")
        Product.objects.create(
            category=category,
            name=tr("Ketler"),
            slug="ketler",
            code="B-083",
            box_weight="1.500",
            shelf_life_months=6,
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            Product.objects.create(
                category=category,
                name=tr("Ketler 2"),
                slug="ketler-2",
                code="B-083",
                box_weight="1.500",
                shelf_life_months=6,
            )

    def test_str_uses_default_language_name(self):
        category = Category.objects.create(name=tr("Круассаны"), slug="croissants", image="c.jpg")
        product = Product.objects.create(
            category=category,
            name={"ru": "Кетлер", "en": "Ketler"},
            slug="ketler",
            code="B-083",
            box_weight="1.500",
            shelf_life_months=6,
        )
        self.assertEqual(str(product), "B-083 — Кетлер")
