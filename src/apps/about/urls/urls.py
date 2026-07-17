from django.urls import path

from apps.about.views import HomeView, TimelineListView

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("timeline/", TimelineListView.as_view(), name="timeline-list"),
]
