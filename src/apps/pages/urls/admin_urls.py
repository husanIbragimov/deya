from django.urls import path

from apps.pages.views.admin import (
    BannerAdminDetailView,
    BannerAdminListCreateView,
    PrivacyPolicyAdminDetailView,
    PrivacyPolicyAdminListCreateView,
    SiteSettingsAdminView,
    StaticPageAdminDetailView,
    StaticPageAdminListCreateView,
)

urlpatterns = [
    path("static-pages/", StaticPageAdminListCreateView.as_view(), name="static-page-admin-list"),
    path("static-pages/<int:pk>/", StaticPageAdminDetailView.as_view(), name="static-page-admin-detail"),
    path("settings/", SiteSettingsAdminView.as_view(), name="site-settings-admin"),
    path("privacy-policy/", PrivacyPolicyAdminListCreateView.as_view(), name="privacy-policy-admin-list"),
    path(
        "privacy-policy/<slug:slug>/",
        PrivacyPolicyAdminDetailView.as_view(),
        name="privacy-policy-admin-detail",
    ),
    path("banners/", BannerAdminListCreateView.as_view(), name="banner-admin-list"),
    path("banners/<int:pk>/", BannerAdminDetailView.as_view(), name="banner-admin-detail"),
]
