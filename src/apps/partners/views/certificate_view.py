from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.partners.selectors import certificates
from apps.partners.serializers import CertificateSerializer


@extend_schema(tags=["Partners"])
class CertificateListView(ListAPIView):
    serializer_class = CertificateSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return certificates()
