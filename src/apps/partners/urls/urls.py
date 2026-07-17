from django.urls import path

from apps.partners.views import CertificateListView, PartnerListView

urlpatterns = [
    path("partners/", PartnerListView.as_view(), name="partner-list"),
    path("certificates/", CertificateListView.as_view(), name="certificate-list"),
]
