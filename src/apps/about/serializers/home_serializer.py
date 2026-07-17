from rest_framework import serializers

from apps.about.serializers.export_region_serializer import ExportRegionSerializer
from apps.about.serializers.home_slide_serializer import HomeSlideSerializer
from apps.about.serializers.stat_serializer import StatSerializer
from apps.blog.serializers import PostListSerializer
from apps.catalog.serializers import CategorySerializer, ProductListSerializer


class HomeSerializer(serializers.Serializer):
    slides = HomeSlideSerializer(many=True)
    stats = StatSerializer(many=True)
    categories = CategorySerializer(many=True)
    featured_products = ProductListSerializer(many=True)
    export_regions = ExportRegionSerializer(many=True)
    latest_posts = PostListSerializer(many=True)
