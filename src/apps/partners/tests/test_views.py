from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.partners.models import Certificate, Partner


class PartnerListViewTests(APITestCase):
    def test_lists_partners(self):
        Partner.objects.create(name="Acme", logo="l.jpg")

        response = self.client.get(reverse("partners:partner-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class CertificateListViewTests(APITestCase):
    def test_lists_certificates(self):
        Certificate.objects.create(title={"ru": "ISO", "en": "ISO"}, image="c.jpg")

        response = self.client.get(reverse("partners:certificate-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
