from django.urls import path

from apps.catalog.views import (
    CategoryListView,
    ProductDetailView,
    ProductListView,
    ProductRelatedView,
)

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
    path("products/<slug:slug>/related/", ProductRelatedView.as_view(), name="product-related"),
]
