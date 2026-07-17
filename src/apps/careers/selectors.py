from django.db.models import QuerySet

from apps.careers.models import CareerValue, Company


def companies() -> QuerySet[Company]:
    return Company.objects.all()


def career_values() -> QuerySet[CareerValue]:
    return CareerValue.objects.all()
