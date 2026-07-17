from django.urls import path

from apps.careers.views.admin import (
    CareerValueAdminDetailView,
    CareerValueAdminListCreateView,
    CompanyAdminDetailView,
    CompanyAdminListCreateView,
)

urlpatterns = [
    path("companies/", CompanyAdminListCreateView.as_view(), name="company-admin-list"),
    path("companies/<int:pk>/", CompanyAdminDetailView.as_view(), name="company-admin-detail"),
    path("career-values/", CareerValueAdminListCreateView.as_view(), name="career-value-admin-list"),
    path("career-values/<int:pk>/", CareerValueAdminDetailView.as_view(), name="career-value-admin-detail"),
]
