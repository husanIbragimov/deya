from django.urls import path

from apps._auth.views.admin import UserAdminCreateView

urlpatterns = [
    path("create/", view=UserAdminCreateView.as_view(), name="user-admin-create"),
]
