from django.urls import path

from apps.about.views.admin import (
    ExportRegionAdminDetailView,
    ExportRegionAdminListCreateView,
    FactoryAdminView,
    HomeSlideAdminDetailView,
    HomeSlideAdminListCreateView,
    ProductInfoAdminDetailView,
    ProductInfoAdminListCreateView,
    StatAdminDetailView,
    StatAdminListCreateView,
    TimelineEventAdminDetailView,
    TimelineEventAdminListCreateView,
)

urlpatterns = [
    path("slides/", HomeSlideAdminListCreateView.as_view(), name="home-slide-admin-list"),
    path("slides/<int:pk>/", HomeSlideAdminDetailView.as_view(), name="home-slide-admin-detail"),
    path("stats/", StatAdminListCreateView.as_view(), name="stat-admin-list"),
    path("stats/<int:pk>/", StatAdminDetailView.as_view(), name="stat-admin-detail"),
    path("timeline/", TimelineEventAdminListCreateView.as_view(), name="timeline-event-admin-list"),
    path("timeline/<int:pk>/", TimelineEventAdminDetailView.as_view(), name="timeline-event-admin-detail"),
    path("export-regions/", ExportRegionAdminListCreateView.as_view(), name="export-region-admin-list"),
    path("export-regions/<int:pk>/", ExportRegionAdminDetailView.as_view(), name="export-region-admin-detail"),
    path("factory/", FactoryAdminView.as_view(), name="factory-admin"),
    path("product-info/", ProductInfoAdminListCreateView.as_view(), name="product-info-admin-list"),
    path("product-info/<int:pk>/", ProductInfoAdminDetailView.as_view(), name="product-info-admin-detail"),
]
