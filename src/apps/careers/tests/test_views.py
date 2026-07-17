from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.careers.models import CareerValue, Company
from apps.careers.tests.helpers import tr


class CompanyListViewTests(APITestCase):
    def test_lists_companies(self):
        Company.objects.create(name="Iruskon", slug="iruskon", image="c.jpg")

        response = self.client.get(reverse("careers:company-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class CareerValueListViewTests(APITestCase):
    def test_lists_career_values(self):
        CareerValue.objects.create(title=tr("Value"), text=tr("Text"))

        response = self.client.get(reverse("careers:career-value-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
