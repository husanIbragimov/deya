from django.urls import path

from apps.partners.views.admin import (
    CertificateAdminDetailView,
    CertificateAdminListCreateView,
    PartnerAdminDetailView,
    PartnerAdminListCreateView,
)

urlpatterns = [
    path("partners/", PartnerAdminListCreateView.as_view(), name="partner-admin-list"),
    path("partners/<int:pk>/", PartnerAdminDetailView.as_view(), name="partner-admin-detail"),
    path("certificates/", CertificateAdminListCreateView.as_view(), name="certificate-admin-list"),
    path("certificates/<int:pk>/", CertificateAdminDetailView.as_view(), name="certificate-admin-detail"),
]
