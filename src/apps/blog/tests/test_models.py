from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from apps.blog.models import Post
from apps.blog.tests.helpers import tr


class PostModelTests(TestCase):
    def test_slug_is_unique(self):
        Post.objects.create(title=tr("First"), slug="first", cover="c.jpg", published_at=timezone.now())
        with self.assertRaises(IntegrityError), transaction.atomic():
            Post.objects.create(title=tr("Second"), slug="first", cover="c.jpg", published_at=timezone.now())

    def test_str_uses_default_language_title(self):
        post = Post.objects.create(
            title={"ru": "Заголовок", "en": "Title"}, slug="post", cover="c.jpg", published_at=timezone.now()
        )
        self.assertEqual(str(post), "Заголовок")
