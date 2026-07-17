from django.db.models import QuerySet

from apps.about.models import ExportRegion, HomeSlide, Stat, TimelineEvent


def home_slides() -> QuerySet[HomeSlide]:
    return HomeSlide.objects.all()


def stats() -> QuerySet[Stat]:
    return Stat.objects.all()


def timeline_events() -> QuerySet[TimelineEvent]:
    return TimelineEvent.objects.all()


def export_regions() -> QuerySet[ExportRegion]:
    return ExportRegion.objects.all()
