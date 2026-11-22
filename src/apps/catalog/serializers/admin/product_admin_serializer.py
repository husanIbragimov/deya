from rest_framework import serializers

from apps.catalog.models import Product
from apps.catalog.serializers.admin.box_quantity_validation import validate_box_quantity
from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.serializers import TranslatedJSONField


class ProductAdminSerializer(serializers.ModelSerializer):
    name = TranslatedJSONField()
    description = TranslatedJSONField(required=False)

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "family",
            "flavor",
            "name",
            "slug",
            "description",
            "code",
            "box_weight",
            "box_quantity",
            "box_quantity_unit",
            "shelf_life_months",
            "weight",
            "badge",
            "is_featured",
            "related_products",
            "sort_order",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        attrs = super().validate(attrs)

        def current(field):
            if field in attrs:
                return attrs[field]
            return getattr(self.instance, field, None)

        validate_box_quantity(current("box_quantity"), current("box_quantity_unit"))

        family = current("family")
        if family is not None:
            duplicates = Product.objects.filter(family=family, flavor=current("flavor"), weight=current("weight"))
            if self.instance is not None:
                duplicates = duplicates.exclude(pk=self.instance.pk)
            if duplicates.exists():
                raise serializers.ValidationError({"weight": str(_(T.product_variant_exists_message))})
        return attrs
