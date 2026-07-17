from .category_admin_view import CategoryAdminDetailView, CategoryAdminListCreateView
from .flavor_admin_view import FlavorAdminDetailView, FlavorAdminListCreateView
from .product_admin_view import ProductAdminDetailView, ProductAdminListCreateView
from .product_family_admin_view import ProductFamilyAdminDetailView, ProductFamilyAdminListCreateView
from .product_image_admin_view import ProductImageAdminDetailView, ProductImageAdminListCreateView
from .weight_admin_view import WeightAdminDetailView, WeightAdminListCreateView

__all__ = [
    "CategoryAdminListCreateView",
    "CategoryAdminDetailView",
    "FlavorAdminListCreateView",
    "FlavorAdminDetailView",
    "WeightAdminListCreateView",
    "WeightAdminDetailView",
    "ProductFamilyAdminListCreateView",
    "ProductFamilyAdminDetailView",
    "ProductAdminListCreateView",
    "ProductAdminDetailView",
    "ProductImageAdminListCreateView",
    "ProductImageAdminDetailView",
]
