from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from apps.catalog.models import (
    Category,
    Flavor,
    Product,
    ProductFamily,
    ProductImage,
    Weight,
)


class JSONWidgetAdminMixin:
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


class ProductImageInline(JSONWidgetAdminMixin, admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "alt", "is_main", "sort_order")


@admin.register(Category)
class CategoryAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    list_display = ("id", "slug", "sort_order", "is_active")
    list_filter = ("is_active",)
    list_editable = ("sort_order", "is_active")
    search_fields = ("name__ru", "name__en", "slug")


@admin.register(Flavor)
class FlavorAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    list_display = ("id", "slug", "sort_order")
    list_editable = ("sort_order",)
    search_fields = ("name__ru", "name__en", "slug")


@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    list_display = ("id", "value", "unit")
    list_filter = ("unit",)


@admin.register(ProductFamily)
class ProductFamilyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    list_display = ("id", "code", "slug", "category", "family", "flavor", "badge", "is_featured", "is_active")
    list_filter = ("category", "family", "flavor", "badge", "is_featured", "is_active")
    list_editable = ("is_featured", "is_active")
    search_fields = ("code", "name__ru", "name__en", "slug")
    filter_horizontal = ("weights", "related_products")
    autocomplete_fields = ("category", "family", "flavor")
    inlines = [ProductImageInline]
