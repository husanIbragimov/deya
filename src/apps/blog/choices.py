from django.db import models

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _


class PostBlockTypeChoice(models.TextChoices):
    HEADING = "heading", _(T.block_type_heading)
    TEXT = "text", _(T.block_type_text)
    IMAGE = "image", _(T.block_type_image)
