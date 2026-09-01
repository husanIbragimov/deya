from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from apps.pages.models import Banner, PrivacyPolicy, SiteSettings, StaticPage


class JSONWidgetAdminMixin:
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(StaticPage)
class StaticPageAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    list_display = ("id", "slug")
    search_fields = ("slug",)


@admin.register(SiteSettings)
class SiteSettingsAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    list_display = ("id", "phone", "email")

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    list_display = ("id", "slug")
    search_fields = ("slug",)


@admin.register(Banner)
class BannerAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    list_display = ("id", "type")
    list_filter = ("type",)
