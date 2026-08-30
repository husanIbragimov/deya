from django.urls import path

from apps.pages.views.admin import (
    PrivacyPolicyAdminView,
    SiteSettingsAdminView,
    StaticPageAdminDetailView,
    StaticPageAdminListCreateView,
)

urlpatterns = [
    path("static-pages/", StaticPageAdminListCreateView.as_view(), name="static-page-admin-list"),
    path("static-pages/<int:pk>/", StaticPageAdminDetailView.as_view(), name="static-page-admin-detail"),
    path("settings/", SiteSettingsAdminView.as_view(), name="site-settings-admin"),
    path("privacy-policy/", PrivacyPolicyAdminView.as_view(), name="privacy-policy-admin"),
]
