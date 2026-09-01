from django.db.models import QuerySet

from apps.pages.models import Banner, PrivacyPolicy, SiteSettings, StaticPage


def get_static_page(slug: str) -> StaticPage:
    return StaticPage.objects.get(slug=slug)


def banners(type_: str | None = None) -> QuerySet[Banner]:
    queryset = Banner.objects.all()
    if type_:
        queryset = queryset.filter(type=type_)
    return queryset


def get_site_settings() -> SiteSettings:
    return SiteSettings.load()


def privacy_policies() -> QuerySet[PrivacyPolicy]:
    return PrivacyPolicy.objects.all()


def get_privacy_policy(slug: str) -> PrivacyPolicy:
    return PrivacyPolicy.objects.get(slug=slug)
