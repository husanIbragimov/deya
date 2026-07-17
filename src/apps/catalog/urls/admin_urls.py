from django.urls import path

from apps.catalog.views.admin import (
    CategoryAdminDetailView,
    CategoryAdminListCreateView,
    FlavorAdminDetailView,
    FlavorAdminListCreateView,
    ProductAdminDetailView,
    ProductAdminListCreateView,
    ProductFamilyAdminDetailView,
    ProductFamilyAdminListCreateView,
    ProductImageAdminDetailView,
    ProductImageAdminListCreateView,
    WeightAdminDetailView,
    WeightAdminListCreateView,
)

urlpatterns = [
    path("categories/", CategoryAdminListCreateView.as_view(), name="category-admin-list"),
    path("categories/<int:pk>/", CategoryAdminDetailView.as_view(), name="category-admin-detail"),
    path("flavors/", FlavorAdminListCreateView.as_view(), name="flavor-admin-list"),
    path("flavors/<int:pk>/", FlavorAdminDetailView.as_view(), name="flavor-admin-detail"),
    path("weights/", WeightAdminListCreateView.as_view(), name="weight-admin-list"),
    path("weights/<int:pk>/", WeightAdminDetailView.as_view(), name="weight-admin-detail"),
    path("product-families/", ProductFamilyAdminListCreateView.as_view(), name="product-family-admin-list"),
    path("product-families/<int:pk>/", ProductFamilyAdminDetailView.as_view(), name="product-family-admin-detail"),
    path("products/", ProductAdminListCreateView.as_view(), name="product-admin-list"),
    path("products/<int:pk>/", ProductAdminDetailView.as_view(), name="product-admin-detail"),
    path("product-images/", ProductImageAdminListCreateView.as_view(), name="product-image-admin-list"),
    path("product-images/<int:pk>/", ProductImageAdminDetailView.as_view(), name="product-image-admin-detail"),
]
