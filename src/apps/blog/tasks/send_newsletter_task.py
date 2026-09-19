from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.defaultfilters import date as format_date
from django.template.loader import render_to_string
from django.urls import reverse

from apps.blog.models import Post
from apps.common.utils.translated_value import translated_value
from apps.leads.models import NewsletterSubscription
from apps.logger._loggers import celeryLogger


@shared_task(bind=True)
def sendBlogNewsletterTask(self, post_id):
    try:
        post = Post.objects.get(pk=post_id, is_published=True)
    except Post.DoesNotExist:
        celeryLogger.warning("sendBlogNewsletterTask: post %s not found or not published, skipping", post_id)
        return "skipped: post not found or not published"

    post_context = {
        "slug": post.slug,
        "cover": post.cover,
        "title": translated_value(post.title),
        "excerpt": translated_value(post.excerpt),
        "published_at": format_date(post.published_at, "j E Y"),
    }
    subject = f"Новое в блоге Deya: {post_context['title']}"

    subscriptions = NewsletterSubscription.objects.filter(is_active=True).values_list("email", "unsubscribe_token")

    sent_count = 0
    for email, unsubscribe_token in subscriptions:
        unsubscribe_url = settings.SITE_URL.rstrip("/") + reverse(
            "leads:subscription-unsubscribe", kwargs={"token": unsubscribe_token}
        )
        html_body = render_to_string(
            "blog-newsletter-deya.html",
            {"post": post_context, "unsubscribe_url": unsubscribe_url},
        )
        try:
            message = EmailMultiAlternatives(
                subject=subject,
                body=post_context["excerpt"],
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )
            message.attach_alternative(html_body, "text/html")
            message.send()
            sent_count += 1
        except Exception:
            celeryLogger.exception("sendBlogNewsletterTask: failed to email %s for post %s", email, post_id)

    return f"sent {sent_count}/{len(subscriptions)}"
