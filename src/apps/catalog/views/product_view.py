from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.catalog.filters import ProductFilter
from apps.catalog.selectors import get_related_products, product_base_queryset
from apps.catalog.serializers import ProductDetailSerializer, ProductListSerializer
from apps.common.pagination import PageNumberPagination


@extend_schema(tags=["Catalog"])
class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter

    def get_queryset(self):
        return product_base_queryset()


@extend_schema(tags=["Catalog"])
class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = (AllowAny,)
    lookup_field = "slug"

    def get_queryset(self):
        return product_base_queryset()


@extend_schema(tags=["Catalog"])
class ProductRelatedView(GenericAPIView):
    serializer_class = ProductListSerializer
    permission_classes = (AllowAny,)
    lookup_field = "slug"

    def get_queryset(self):
        return product_base_queryset()

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        related = get_related_products(product)
        serializer = self.get_serializer(related, many=True)
        return Response(serializer.data)
