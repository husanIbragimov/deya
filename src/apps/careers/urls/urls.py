from django.urls import path

from apps.careers.views import CareerValueListView, CompanyListView

urlpatterns = [
    path("companies/", CompanyListView.as_view(), name="company-list"),
    path("career-values/", CareerValueListView.as_view(), name="career-value-list"),
]
