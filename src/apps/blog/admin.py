from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from apps.blog.models import Post, PostBlock


class JSONWidgetAdminMixin:
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


class PostBlockInline(JSONWidgetAdminMixin, admin.TabularInline):
    model = PostBlock
    extra = 1
    fields = ("type", "text", "image", "sort_order")


@admin.register(Post)
class PostAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    list_display = ("id", "slug", "published_at", "is_published")
    list_filter = ("is_published",)
    list_editable = ("is_published",)
    search_fields = ("title__ru", "title__en", "slug")
    inlines = [PostBlockInline]
