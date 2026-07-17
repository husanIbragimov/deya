from apps.pages.models import SiteSettings, StaticPage


def get_static_page(slug: str) -> StaticPage:
    return StaticPage.objects.get(slug=slug)


def get_site_settings() -> SiteSettings:
    return SiteSettings.load()
