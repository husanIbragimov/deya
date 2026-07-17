from django.db.models import QuerySet

from apps.leads.models import Lead, NewsletterSubscription


def admin_leads() -> QuerySet[Lead]:
    return Lead.objects.select_related("product").all()


def admin_subscriptions() -> QuerySet[NewsletterSubscription]:
    return NewsletterSubscription.objects.all()
