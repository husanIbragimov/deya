from django.core import mail
from django.test import TestCase
from django.utils import timezone

from apps.blog.models import Post
from apps.blog.tasks import sendBlogNewsletterTask
from apps.blog.tests.helpers import tr
from apps.leads.models import NewsletterSubscription


def make_post(slug="news", **kwargs):
    defaults = dict(
        title=tr("News title"),
        excerpt=tr("News excerpt"),
        cover="c.jpg",
        published_at=timezone.now(),
        is_published=True,
    )
    defaults.update(kwargs)
    return Post.objects.create(slug=slug, **defaults)


class SendBlogNewsletterTaskTests(TestCase):
    def test_emails_only_active_subscribers(self):
        NewsletterSubscription.objects.create(email="active-one@example.com", is_active=True)
        NewsletterSubscription.objects.create(email="active-two@example.com", is_active=True)
        NewsletterSubscription.objects.create(email="inactive@example.com", is_active=False)
        post = make_post()

        sendBlogNewsletterTask(post_id=post.id)

        self.assertEqual(len(mail.outbox), 2)
        recipients = {message.to[0] for message in mail.outbox}
        self.assertEqual(recipients, {"active-one@example.com", "active-two@example.com"})
        self.assertIn("News title", mail.outbox[0].subject)
        self.assertIn("News title", mail.outbox[0].alternatives[0][0])

    def test_skips_unpublished_post(self):
        NewsletterSubscription.objects.create(email="active@example.com", is_active=True)
        post = make_post(is_published=False)

        sendBlogNewsletterTask(post_id=post.id)

        self.assertEqual(len(mail.outbox), 0)

    def test_no_active_subscribers_sends_nothing(self):
        post = make_post()

        result = sendBlogNewsletterTask(post_id=post.id)

        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(result, "sent 0/0")
