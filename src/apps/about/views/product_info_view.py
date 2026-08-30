from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.about.selectors import product_infos
from apps.about.serializers import ProductInfoSerializer


@extend_schema(tags=["About"])
class ProductInfoListView(ListAPIView):
    serializer_class = ProductInfoSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return product_infos()
