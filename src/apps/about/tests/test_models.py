from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.about.models import TimelineEvent
from apps.about.tests.helpers import tr


class TimelineEventModelTests(TestCase):
    def test_year_is_unique(self):
        TimelineEvent.objects.create(year=1994, title=tr("Founded"))
        with self.assertRaises(IntegrityError), transaction.atomic():
            TimelineEvent.objects.create(year=1994, title=tr("Founded again"))

    def test_str_includes_year_and_title(self):
        event = TimelineEvent.objects.create(year=2026, title={"ru": "Событие", "en": "Event"})
        self.assertEqual(str(event), "2026 — Событие")
