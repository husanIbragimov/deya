from django.db.models import QuerySet

from apps.about.models import (
    ExportRegion,
    Factory,
    HomeSlide,
    ProductInfo,
    Stat,
    TimelineEvent,
)


def home_slides() -> QuerySet[HomeSlide]:
    return HomeSlide.objects.filter(is_active=True)


def get_factory() -> Factory:
    return Factory.load()


def product_infos() -> QuerySet[ProductInfo]:
    return ProductInfo.objects.all()


def stats() -> QuerySet[Stat]:
    return Stat.objects.filter(is_active=True)


def timeline_events() -> QuerySet[TimelineEvent]:
    return TimelineEvent.objects.all()


def export_regions() -> QuerySet[ExportRegion]:
    return ExportRegion.objects.all()
