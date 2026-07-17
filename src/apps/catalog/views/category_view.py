from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.catalog.selectors import active_categories
from apps.catalog.serializers import CategorySerializer


@extend_schema(tags=["Catalog"])
class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return active_categories()
