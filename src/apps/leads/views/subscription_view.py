from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from apps.common.base_api import BaseGenericAPI
from apps.leads.serializers import (
    SubscriptionCreateSerializer,
    UnsubscribeResultSerializer,
)
from apps.leads.services import subscribe, unsubscribe


@extend_schema(tags=["Leads"])
class SubscriptionCreateView(BaseGenericAPI):
    serializer_class = SubscriptionCreateSerializer
    permission_classes = (AllowAny,)
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = "subscription"

    def post(self, request, *args, **kwargs):
        subscription = subscribe(self.validate_data["email"])
        return Response({"email": subscription.email}, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Leads"])
class UnsubscribeView(GenericAPIView):
    serializer_class = UnsubscribeResultSerializer
    permission_classes = (AllowAny,)

    def get(self, request, token, *args, **kwargs):
        subscription = unsubscribe(token)
        return Response(self.get_serializer(subscription).data)
