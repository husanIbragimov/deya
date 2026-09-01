from django.urls import path

from apps.pages.views import (
    BannerListView,
    PrivacyPolicyDetailView,
    PrivacyPolicyListView,
    SiteSettingsView,
    StaticPageDetailView,
)

urlpatterns = [
    path("settings/", SiteSettingsView.as_view(), name="site-settings"),
    path("pages/<slug:slug>/", StaticPageDetailView.as_view(), name="static-page-detail"),
    path("privacy-policy/", PrivacyPolicyListView.as_view(), name="privacy-policy-list"),
    path("privacy-policy/<slug:slug>/", PrivacyPolicyDetailView.as_view(), name="privacy-policy-detail"),
    path("banners/", BannerListView.as_view(), name="banner-list"),
]
