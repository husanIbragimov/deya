from django.urls import path

from apps._auth.views import SetPasswordAPIView, UserMeView

urlpatterns = [
    path("me/", view=UserMeView.as_view(), name="user_me_view"),
    path("set-password/", view=SetPasswordAPIView.as_view(), name="set-password"),
]
