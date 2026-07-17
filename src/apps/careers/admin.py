from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from apps.careers.models import CareerValue, Company


class JSONWidgetAdminMixin:
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(Company)
class CompanyAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(CareerValue)
class CareerValueAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    list_display = ("id",)
