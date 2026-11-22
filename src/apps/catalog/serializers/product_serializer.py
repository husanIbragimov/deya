from rest_framework import serializers

from apps.catalog.choices import BoxQuantityUnitChoice
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


class ProductVariantSerializer(ProductListSerializer):
    weight = WeightSerializer(read_only=True)

    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + ("weight",)


class ProductDetailSerializer(serializers.ModelSerializer):
    name = TranslatedField()
    description = TranslatedField()
    category = CategorySerializer(read_only=True)
    flavor = FlavorSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    weight = WeightSerializer(read_only=True)
    variants = serializers.SerializerMethodField()
    # Variant's own value, or the family's shared value when the variant has none.
    box_quantity = serializers.DecimalField(
        source="effective_box_quantity", max_digits=10, decimal_places=3, read_only=True, allow_null=True
    )
    box_quantity_unit = serializers.ChoiceField(
        source="effective_box_quantity_unit", choices=BoxQuantityUnitChoice.choices, read_only=True, allow_blank=True
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "code",
            "box_weight",
            "box_quantity",
            "box_quantity_unit",
            "shelf_life_months",
            "category",
            "flavor",
            "badge",
            "is_featured",
            "images",
            "weight",
            "variants",
        )

    def get_variants(self, obj):
        from apps.catalog.selectors import get_family_variants

        return ProductVariantSerializer(get_family_variants(obj), many=True, context=self.context).data
