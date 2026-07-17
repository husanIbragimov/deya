from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.careers.models import Company


class CompanyModelTests(TestCase):
    def test_slug_is_unique(self):
        Company.objects.create(name="Iruskon", slug="iruskon", image="c.jpg")
        with self.assertRaises(IntegrityError), transaction.atomic():
            Company.objects.create(name="Iruskon 2", slug="iruskon", image="c.jpg")
