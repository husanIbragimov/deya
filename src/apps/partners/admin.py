from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from apps.partners.models import Certificate, Partner


class JSONWidgetAdminMixin:
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "website")
    search_fields = ("name",)


@admin.register(Certificate)
class CertificateAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    list_display = ("id",)
