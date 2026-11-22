from rest_framework import serializers

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _


def validate_box_quantity(quantity, unit) -> None:
    """Quantity per box and its unit must be set together (mirrors the model's check constraint)."""
    if quantity is not None and not unit:
        raise serializers.ValidationError({"box_quantity_unit": str(_(T.box_quantity_unit_required_message))})
    if quantity is None and unit:
        raise serializers.ValidationError({"box_quantity": str(_(T.box_quantity_required_message))})
