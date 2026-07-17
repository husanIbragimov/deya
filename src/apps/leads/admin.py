from django.contrib import admin

from apps.leads.models import Lead, NewsletterSubscription


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "name", "phone", "status", "created_at")
    list_filter = ("type", "status")
    list_editable = ("status",)
    search_fields = ("name", "email", "phone")
    readonly_fields = ("source_url", "ip_address", "user_agent", "created_at", "updated_at")


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("email",)
    readonly_fields = ("unsubscribe_token",)
