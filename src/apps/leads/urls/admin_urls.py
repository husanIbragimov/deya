from django.urls import path

from apps.leads.views.admin import (
    LeadAdminDetailView,
    LeadAdminListView,
    LeadStatusUpdateView,
    SubscriptionAdminDetailView,
    SubscriptionAdminListView,
)

urlpatterns = [
    path("leads/", LeadAdminListView.as_view(), name="lead-admin-list"),
    path("leads/<int:pk>/", LeadAdminDetailView.as_view(), name="lead-admin-detail"),
    path("leads/<int:pk>/status/", LeadStatusUpdateView.as_view(), name="lead-admin-status-update"),
    path("subscriptions/", SubscriptionAdminListView.as_view(), name="subscription-admin-list"),
    path("subscriptions/<int:pk>/", SubscriptionAdminDetailView.as_view(), name="subscription-admin-detail"),
]
