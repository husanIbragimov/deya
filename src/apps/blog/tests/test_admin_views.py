import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps._auth.models import User
from apps.blog.models import Post


class PostAdminCrudTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)

    def test_create_and_delete_flow(self):
        create_response = self.client.post(
            reverse("blog-admin:post-admin-list"),
            data={
                "title": json.dumps({"ru": "Новость", "en": "News"}),
                "slug": "news",
                "cover": "news-cover.jpg",
                "published_at": "2026-01-01T00:00:00Z",
                "is_published": True,
            },
            format="multipart",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED, create_response.data)
        post_id = create_response.data["id"]

        delete_response = self.client.delete(reverse("blog-admin:post-admin-detail", kwargs={"pk": post_id}))
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=post_id).exists())
