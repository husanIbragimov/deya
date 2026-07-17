from django.db import models

from apps.blog.choices import PostBlockTypeChoice
from apps.blog.models.post import Post
from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.models import BaseModel


class PostBlock(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="blocks", verbose_name=_(T.post))
    type = models.CharField(max_length=16, choices=PostBlockTypeChoice.choices, verbose_name=_(T.block_type))
    text = models.JSONField(default=dict, blank=True, verbose_name=_(T.text))
    image = models.CharField(max_length=500, blank=True, verbose_name=_(T.image))
    sort_order = models.PositiveSmallIntegerField(default=0, db_index=True, verbose_name=_(T.sort_order))

    class Meta:
        ordering = ("sort_order", "id")
        verbose_name = _(T.post_block)
        verbose_name_plural = _(T.post_blocks)

    def __str__(self):
        return f"{self.post_id}:{self.type}"
