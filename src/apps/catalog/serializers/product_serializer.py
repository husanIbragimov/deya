from rest_framework import serializers

from apps.catalog.models import Product
from apps.catalog.serializers.category_serializer import CategorySerializer
from apps.catalog.serializers.flavor_serializer import FlavorSerializer
from apps.catalog.serializers.product_image_serializer import ProductImageSerializer
from apps.catalog.serializers.weight_serializer import WeightSerializer
from apps.common.serializers import TranslatedField


class ProductListSerializer(serializers.ModelSerializer):
    name = TranslatedField()
    category = CategorySerializer(read_only=True)
    flavor = FlavorSerializer(read_only=True)
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "name", "slug", "category", "flavor", "badge", "is_featured", "main_image")

    def get_main_image(self, obj):
        images = list(obj.images.all())
        image = next((img for img in images if img.is_main), images[0] if images else None)
        if not image:
            return None
        return ProductImageSerializer(image, context=self.context).data


class ProductDetailSerializer(serializers.ModelSerializer):
    name = TranslatedField()
    description = TranslatedField()
    category = CategorySerializer(read_only=True)
    flavor = FlavorSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    weights = WeightSerializer(many=True, read_only=True)
    variants = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "code",
            "box_weight",
            "shelf_life_months",
            "category",
            "flavor",
            "badge",
            "is_featured",
            "images",
            "weights",
            "variants",
        )

    def get_variants(self, obj):
        from apps.catalog.selectors import get_family_variants

        return ProductListSerializer(get_family_variants(obj), many=True, context=self.context).data
