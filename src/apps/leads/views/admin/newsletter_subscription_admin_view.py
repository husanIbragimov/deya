from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser

from apps.leads.selectors import admin_subscriptions
from apps.leads.serializers.admin import NewsletterSubscriptionAdminSerializer


@extend_schema(tags=["Leads Admin"])
class SubscriptionAdminListView(ListAPIView):
    serializer_class = NewsletterSubscriptionAdminSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return admin_subscriptions()


@extend_schema(tags=["Leads Admin"])
class SubscriptionAdminDetailView(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    serializer_class = NewsletterSubscriptionAdminSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return admin_subscriptions()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
