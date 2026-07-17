from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.blog.models import Post, PostBlock
from apps.blog.tests.helpers import tr


def make_post(slug, **kwargs):
    defaults = dict(title=tr(slug), cover="c.jpg", published_at=timezone.now(), is_published=True)
    defaults.update(kwargs)
    return Post.objects.create(slug=slug, **defaults)


class PostListViewTests(APITestCase):
    def test_only_published_posts_are_listed(self):
        make_post("published")
        make_post("draft", is_published=False)

        response = self.client.get(reverse("blog:post-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        slugs = [item["slug"] for item in response.data["results"]]
        self.assertEqual(slugs, ["published"])


class PostDetailViewTests(APITestCase):
    def test_detail_includes_blocks_and_other_posts(self):
        post = make_post("main")
        make_post("sibling")
        PostBlock.objects.create(post=post, type="heading", text=tr("Hello"), sort_order=1)

        response = self.client.get(reverse("blog:post-detail", kwargs={"slug": post.slug}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["blocks"]), 1)
        self.assertEqual([p["slug"] for p in response.data["other_posts"]], ["sibling"])
