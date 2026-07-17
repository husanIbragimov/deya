from rest_framework import status

from apps.common.locale import TranslatableText as T
from apps.common.locale import getTextLazy as _
from apps.common.response import ExceptionResponse, ResponseCode
from apps.leads.models import NewsletterSubscription


def subscribe(email: str) -> NewsletterSubscription:
    subscription, created = NewsletterSubscription.objects.get_or_create(email=email)
    if not created and not subscription.is_active:
        subscription.is_active = True
        subscription.save(update_fields=["is_active"])
    return subscription


def unsubscribe(token: str) -> NewsletterSubscription:
    try:
        subscription = NewsletterSubscription.objects.get(unsubscribe_token=token)
    except (NewsletterSubscription.DoesNotExist, ValueError):
        raise ExceptionResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            response_code=ResponseCode.UNSUBSCRIBE_TOKEN_INVALID,
            detail=str(_(T.unsubscribe_token_invalid_message)),
        )
    subscription.is_active = False
    subscription.save(update_fields=["is_active"])
    return subscription
