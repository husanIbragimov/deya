from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from apps.about.models import ExportRegion, HomeSlide, Stat, TimelineEvent


class JSONWidgetAdminMixin:
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(HomeSlide)
class HomeSlideAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    list_display = ("id", "cta_url")


@admin.register(Stat)
class StatAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    list_display = ("id", "value")


@admin.register(TimelineEvent)
class TimelineEventAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    list_display = ("id", "year")
    list_filter = ("year",)


@admin.register(ExportRegion)
class ExportRegionAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    list_display = ("id", "position_x", "position_y")
