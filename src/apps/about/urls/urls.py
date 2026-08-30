from django.urls import path

from apps.about.views import (
    FactoryView,
    HomeView,
    ProductInfoListView,
    TimelineListView,
)

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("timeline/", TimelineListView.as_view(), name="timeline-list"),
    path("factory/", FactoryView.as_view(), name="factory"),
    path("product-info/", ProductInfoListView.as_view(), name="product-info-list"),
]
