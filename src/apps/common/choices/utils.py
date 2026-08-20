from functools import reduce
from typing import Type

from django.db.models import Choices
from django.utils.text import format_lazy


def choices_help_text(choices_class: Type[Choices]) -> str:
    """Lazily render a Choices class as "value - label" pairs for use as a field's help_text.

    Keeping this lazy (via format_lazy) matters: the choices' labels are themselves
    lazy translations, and a model field's help_text is only resolved per-request
    (e.g. by drf-spectacular/DRF), so eager string-building here would bake in
    whatever locale was active at import time instead of the requester's locale.
    """
    entries = [format_lazy("{} - {}", value, label) for value, label in choices_class.choices]
    if not entries:
        return ""
    return reduce(lambda a, b: format_lazy("{}, {}", a, b), entries)
