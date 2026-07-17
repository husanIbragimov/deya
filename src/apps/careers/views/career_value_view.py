from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.careers.selectors import career_values
from apps.careers.serializers import CareerValueSerializer


@extend_schema(tags=["Careers"])
class CareerValueListView(ListAPIView):
    serializer_class = CareerValueSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return career_values()
