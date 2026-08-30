from .export_region_admin_view import ExportRegionAdminDetailView, ExportRegionAdminListCreateView
from .factory_admin_view import FactoryAdminView
from .home_slide_admin_view import HomeSlideAdminDetailView, HomeSlideAdminListCreateView
from .product_info_admin_view import ProductInfoAdminDetailView, ProductInfoAdminListCreateView
from .stat_admin_view import StatAdminDetailView, StatAdminListCreateView
from .timeline_event_admin_view import TimelineEventAdminDetailView, TimelineEventAdminListCreateView

__all__ = [
    "HomeSlideAdminListCreateView",
    "HomeSlideAdminDetailView",
    "StatAdminListCreateView",
    "StatAdminDetailView",
    "TimelineEventAdminListCreateView",
    "TimelineEventAdminDetailView",
    "ExportRegionAdminListCreateView",
    "ExportRegionAdminDetailView",
    "FactoryAdminView",
    "ProductInfoAdminListCreateView",
    "ProductInfoAdminDetailView",
]
