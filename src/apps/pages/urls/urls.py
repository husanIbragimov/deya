from django.urls import path

from apps.pages.views import SiteSettingsView, StaticPageDetailView

urlpatterns = [
    path("settings/", SiteSettingsView.as_view(), name="site-settings"),
    path("pages/<slug:slug>/", StaticPageDetailView.as_view(), name="static-page-detail"),
]
