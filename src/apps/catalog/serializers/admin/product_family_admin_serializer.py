from rest_framework import serializers

from apps.catalog.models import ProductFamily
from apps.catalog.serializers.admin.box_quantity_validation import validate_box_quantity


class ProductFamilyAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFamily
        fields = ("id", "name", "slug", "box_quantity", "box_quantity_unit", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        attrs = super().validate(attrs)

        def current(field):
            if field in attrs:
                return attrs[field]
            return getattr(self.instance, field, None)

        validate_box_quantity(current("box_quantity"), current("box_quantity_unit"))
        return attrs
