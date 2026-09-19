import json
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps._auth.models import User
from apps.blog.models import Post


class PostAdminCrudTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)
        self.patcher = patch("apps.blog.views.admin.post_admin_view.sendBlogNewsletterTask.delay")
        self.mock_delay = self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def _payload(self, **overrides):
        payload = {
            "title": json.dumps({"uz": "Yangilik", "ru": "Новость", "en": "News"}),
            "slug": "news",
            "cover": "news-cover.jpg",
            "published_at": "2026-01-01T00:00:00Z",
            "is_published": True,
        }
        payload.update(overrides)
        return payload

    def test_create_and_delete_flow(self):
        create_response = self.client.post(
            reverse("blog-admin:post-admin-list"), data=self._payload(), format="multipart"
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED, create_response.data)
        post_id = create_response.data["id"]

        delete_response = self.client.delete(reverse("blog-admin:post-admin-detail", kwargs={"pk": post_id}))
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=post_id).exists())

    def test_publishing_a_post_dispatches_newsletter_task(self):
        create_response = self.client.post(
            reverse("blog-admin:post-admin-list"), data=self._payload(), format="multipart"
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED, create_response.data)
        self.mock_delay.assert_called_once_with(post_id=create_response.data["id"])

    def test_creating_a_draft_does_not_dispatch_newsletter_task(self):
        create_response = self.client.post(
            reverse("blog-admin:post-admin-list"),
            data=self._payload(slug="draft-news", is_published=False),
            format="multipart",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED, create_response.data)
        self.mock_delay.assert_not_called()
