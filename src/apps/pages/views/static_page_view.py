from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from apps.pages.models import StaticPage
from apps.pages.serializers import StaticPageSerializer


@extend_schema(tags=["Pages"])
class StaticPageDetailView(RetrieveAPIView):
    queryset = StaticPage.objects.all()
    serializer_class = StaticPageSerializer
    permission_classes = (AllowAny,)
    lookup_field = "slug"
