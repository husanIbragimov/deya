from django.conf import settings


def translated_value(data: dict[str, str] | str) -> str:
    """Best-effort plain-text display for a {"ru": "...", "en": "..."} JSONField value.

    Used in __str__/admin list_display, where there's no per-request active language.
    Legacy plain-string values (pre-dating the translation dict schema) are returned unchanged.
    """
    if not data:
        return ""
    if isinstance(data, str):
        return data
    value = data.get(settings.LANGUAGE_CODE)
    if value:
        return value
    return next(iter(data.values()), "")
