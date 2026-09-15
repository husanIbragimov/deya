from django.urls import path

from apps._auth.views.admin import UserAdminCreateView, UserAdminSetPasswordView

urlpatterns = [
    path("create/", view=UserAdminCreateView.as_view(), name="user-admin-create"),
    path(
        "<int:pk>/set-password/",
        view=UserAdminSetPasswordView.as_view(),
        name="user-admin-set-password",
    ),
]
