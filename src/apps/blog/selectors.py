from django.db.models import QuerySet
from django.utils import timezone

from apps.blog.models import Post


def published_posts() -> QuerySet[Post]:
    return Post.objects.filter(is_published=True, published_at__lte=timezone.now()).order_by("-published_at")


def get_post_by_slug(slug: str) -> Post:
    return published_posts().prefetch_related("blocks").get(slug=slug)


def other_posts(post: Post, limit: int = 3) -> QuerySet[Post]:
    return published_posts().exclude(pk=post.pk)[:limit]


def latest_posts(limit: int = 4) -> QuerySet[Post]:
    return published_posts()[:limit]
