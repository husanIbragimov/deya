from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.blog.models import Post
from apps.blog.selectors import get_post_by_slug, other_posts, published_posts
from apps.blog.tests.helpers import tr


def make_post(slug, **kwargs):
    defaults = dict(title=tr(slug), cover="c.jpg", published_at=timezone.now(), is_published=True)
    defaults.update(kwargs)
    return Post.objects.create(slug=slug, **defaults)


class PublishedPostsTests(TestCase):
    def test_excludes_unpublished_and_future_posts(self):
        make_post("published")
        make_post("draft", is_published=False)
        make_post("future", published_at=timezone.now() + timedelta(days=1))

        self.assertEqual([p.slug for p in published_posts()], ["published"])

    def test_ordered_newest_first(self):
        older = make_post("older", published_at=timezone.now() - timedelta(days=2))
        newer = make_post("newer", published_at=timezone.now() - timedelta(days=1))

        self.assertEqual(list(published_posts()), [newer, older])


class OtherPostsTests(TestCase):
    def test_excludes_current_post_and_respects_limit(self):
        current = make_post("current")
        make_post("other-1")
        make_post("other-2")
        make_post("other-3")
        make_post("other-4")

        result = list(other_posts(current, limit=3))

        self.assertNotIn(current, result)
        self.assertEqual(len(result), 3)


class GetPostBySlugTests(TestCase):
    def test_unpublished_post_is_not_found(self):
        make_post("draft", is_published=False)

        with self.assertRaises(Post.DoesNotExist):
            get_post_by_slug("draft")
