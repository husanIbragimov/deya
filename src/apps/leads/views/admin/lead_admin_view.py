from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.common.base_api import BaseGenericUpdateAPI
from apps.leads.selectors import admin_leads
from apps.leads.serializers.admin import LeadAdminSerializer, LeadStatusUpdateSerializer


@extend_schema(tags=["Leads Admin"])
class LeadAdminListView(ListAPIView):
    serializer_class = LeadAdminSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return admin_leads()


@extend_schema(tags=["Leads Admin"])
class LeadAdminDetailView(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    serializer_class = LeadAdminSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return admin_leads()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@extend_schema(tags=["Leads Admin"])
class LeadStatusUpdateView(BaseGenericUpdateAPI):
    serializer_class = LeadStatusUpdateSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return admin_leads()

    def put(self, request, *args, **kwargs):
        instance = self.serializer.save()
        return Response(LeadAdminSerializer(instance).data)

    def patch(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)
