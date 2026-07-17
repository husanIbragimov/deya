from django.urls import path

from apps.blog.views.admin import (
    PostAdminDetailView,
    PostAdminListCreateView,
    PostBlockAdminDetailView,
    PostBlockAdminListCreateView,
)

urlpatterns = [
    path("posts/", PostAdminListCreateView.as_view(), name="post-admin-list"),
    path("posts/<int:pk>/", PostAdminDetailView.as_view(), name="post-admin-detail"),
    path("post-blocks/", PostBlockAdminListCreateView.as_view(), name="post-block-admin-list"),
    path("post-blocks/<int:pk>/", PostBlockAdminDetailView.as_view(), name="post-block-admin-detail"),
]
