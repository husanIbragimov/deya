from .banner_admin_view import BannerAdminDetailView, BannerAdminListCreateView
from .privacy_policy_admin_view import PrivacyPolicyAdminDetailView, PrivacyPolicyAdminListCreateView
from .site_settings_admin_view import SiteSettingsAdminView
from .static_page_admin_view import StaticPageAdminDetailView, StaticPageAdminListCreateView

__all__ = [
    "StaticPageAdminListCreateView",
    "StaticPageAdminDetailView",
    "SiteSettingsAdminView",
    "PrivacyPolicyAdminListCreateView",
    "PrivacyPolicyAdminDetailView",
    "BannerAdminListCreateView",
    "BannerAdminDetailView",
]
