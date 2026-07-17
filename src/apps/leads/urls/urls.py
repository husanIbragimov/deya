from django.urls import path

from apps.leads.views import LeadCreateView, SubscriptionCreateView, UnsubscribeView

urlpatterns = [
    path("leads/", LeadCreateView.as_view(), name="lead-create"),
    path("subscriptions/", SubscriptionCreateView.as_view(), name="subscription-create"),
    path("subscriptions/unsubscribe/<uuid:token>/", UnsubscribeView.as_view(), name="subscription-unsubscribe"),
]
