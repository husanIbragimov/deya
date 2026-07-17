from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.about.models import ExportRegion, HomeSlide, Stat, TimelineEvent
from apps.about.tests.helpers import tr
from apps.blog.tests.helpers import tr as blog_tr
from apps.catalog.models import Category
from apps.catalog.tests.helpers import tr as catalog_tr


class TimelineListViewTests(APITestCase):
    def test_lists_events_ordered_by_year(self):
        TimelineEvent.objects.create(year=2026, title=tr("Now"))
        TimelineEvent.objects.create(year=1994, title=tr("Founded"))

        response = self.client.get(reverse("about:timeline-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["year"] for item in response.data], [1994, 2026])


class HomeViewTests(APITestCase):
    def test_aggregates_all_sections(self):
        from django.utils import timezone

        from apps.blog.models import Post

        HomeSlide.objects.create(title=tr("Slide"), image="s.jpg")
        Stat.objects.create(value="32+", label=tr("countries"))
        Category.objects.create(name=catalog_tr("Круассаны"), slug="croissants", image="c.jpg", is_active=True)
        ExportRegion.objects.create(name=tr("Азия"), position_x="10.00", position_y="20.00")
        Post.objects.create(title=blog_tr("News"), slug="news", cover="c.jpg", published_at=timezone.now())

        response = self.client.get(reverse("about:home"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["slides"]), 1)
        self.assertEqual(len(response.data["stats"]), 1)
        self.assertEqual(len(response.data["categories"]), 1)
        self.assertEqual(len(response.data["export_regions"]), 1)
        self.assertEqual(len(response.data["latest_posts"]), 1)
        self.assertEqual(response.data["featured_products"], [])
