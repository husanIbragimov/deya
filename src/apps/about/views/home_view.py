from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.about.selectors import export_regions, home_slides, stats
from apps.about.serializers.home_serializer import HomeSerializer
from apps.blog.selectors import latest_posts
from apps.catalog.selectors import active_categories, featured_products


@extend_schema(tags=["About"])
class HomeView(GenericAPIView):
    serializer_class = HomeSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        data = {
            "slides": home_slides(),
            "stats": stats(),
            "categories": active_categories(),
            "featured_products": featured_products(),
            "export_regions": export_regions(),
            "latest_posts": latest_posts(),
        }
        serializer = self.get_serializer(data)
        return Response(serializer.data)
