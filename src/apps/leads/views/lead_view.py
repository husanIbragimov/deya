from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from apps.common.base_api import BaseGenericAPI
from apps.leads.serializers import LeadCreateSerializer
from apps.leads.services import CreateLeadDTO, create_lead


@extend_schema(tags=["Leads"])
class LeadCreateView(BaseGenericAPI):
    serializer_class = LeadCreateSerializer
    permission_classes = (AllowAny,)
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = "lead"

    def post(self, request, *args, **kwargs):
        data = self.validate_data
        dto = CreateLeadDTO(
            type=data["type"],
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            message=data.get("message", ""),
            product=data.get("product"),
            consent_personal_data=data["consent_personal_data"],
            consent_marketing=data.get("consent_marketing", False),
            source_url=request.META.get("HTTP_REFERER", ""),
            ip_address=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
        )
        lead = create_lead(dto)
        return Response(self.get_serializer(lead).data, status=status.HTTP_201_CREATED)
