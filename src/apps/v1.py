from django.urls import include, path

urlpatterns = [
    path(
        "auth/",
        include(("apps._auth.urls.auth_urls", "auth"), namespace="auth"),
    ),
    path(
        "user/",
        include(("apps._auth.urls.user_urls", "user"), namespace="user"),
    ),
    path("upload/", include(("apps.upload.urls", "upload"), namespace="upload")),
    path("", include(("apps.catalog.urls.urls", "catalog"), namespace="catalog")),
    path("admin/catalog/", include(("apps.catalog.urls.admin_urls", "catalog"), namespace="catalog-admin")),
    path("", include(("apps.blog.urls.urls", "blog"), namespace="blog")),
    path("admin/blog/", include(("apps.blog.urls.admin_urls", "blog"), namespace="blog-admin")),
    path("", include(("apps.about.urls.urls", "about"), namespace="about")),
    path("admin/about/", include(("apps.about.urls.admin_urls", "about"), namespace="about-admin")),
    path("", include(("apps.careers.urls.urls", "careers"), namespace="careers")),
    path("admin/careers/", include(("apps.careers.urls.admin_urls", "careers"), namespace="careers-admin")),
    path("", include(("apps.partners.urls.urls", "partners"), namespace="partners")),
    path("admin/partners/", include(("apps.partners.urls.admin_urls", "partners"), namespace="partners-admin")),
    path("", include(("apps.pages.urls.urls", "pages"), namespace="pages")),
    path("admin/pages/", include(("apps.pages.urls.admin_urls", "pages"), namespace="pages-admin")),
    path("", include(("apps.leads.urls.urls", "leads"), namespace="leads")),
    path("admin/leads/", include(("apps.leads.urls.admin_urls", "leads"), namespace="leads-admin")),
]
