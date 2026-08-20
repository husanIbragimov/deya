from drf_spectacular.openapi import AutoSchema
from rest_framework.fields import ChoiceField
from rest_framework.serializers import BaseSerializer, ListSerializer


class CustomAutoSchema(AutoSchema):
    """Appends writable choice fields' "value - label" options to create/update descriptions.

    Model choice fields already carry this info via `help_text` (see
    `apps.common.choices.choices_help_text`), which drf-spectacular surfaces per-field in the
    request body schema. That's only visible once a field is expanded though, so this repeats
    it at the top of the operation description for POST/PUT/PATCH, where the frontend sees it
    without digging into each field.
    """

    def get_description(self) -> str:
        description = super().get_description() or ""
        choices_text = self._choices_description()
        if not choices_text:
            return description
        return f"{description}\n\n{choices_text}" if description else choices_text

    def _choices_description(self) -> str:
        if self.method not in ("POST", "PUT", "PATCH"):
            return ""

        serializer = self.get_request_serializer()
        if isinstance(serializer, ListSerializer):
            serializer = serializer.child
        if not isinstance(serializer, BaseSerializer):
            return ""

        lines = []
        for name, field in serializer.fields.items():
            if field.read_only or not isinstance(field, ChoiceField):
                continue
            options = ", ".join(f"{value} - {label}" for value, label in field.choices.items())
            lines.append(f"- **{name}**: {options}")

        if not lines:
            return ""
        return "Available choices:\n" + "\n".join(lines)
