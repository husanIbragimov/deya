from django.db.models import QuerySet

from apps.partners.models import Certificate, Partner


def partners() -> QuerySet[Partner]:
    return Partner.objects.all()


def certificates() -> QuerySet[Certificate]:
    return Certificate.objects.all()
