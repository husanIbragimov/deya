from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt.tokens import RefreshToken

from apps._auth.models import User


class AuthService:
    @classmethod
    def auth_token(cls, username: str, password: str) -> dict[str, str]:
        """
        Authenticate _auth and return access and refresh tokens.
        """
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials")

        refresh = RefreshToken.for_user(user)

        return {"access": str(refresh.access_token), "refresh": str(refresh)}

    @classmethod
    def logout(cls, refresh_token: str) -> None:
        """
        Blacklist the refresh token.
        """
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            raise AuthenticationFailed("Invalid token") from e

    @classmethod
    def set_password(cls, user: User, raw_password: str) -> None:
        """
        Set a new password for the user and log it out of every existing session.
        """
        user.set_password(raw_password)
        user.save(update_fields=["password"])
        cls.logout_all_sessions(user)

    @classmethod
    def logout_all_sessions(cls, user: User) -> None:
        """
        Blacklist every outstanding refresh token for the user.
        """
        for token in OutstandingToken.objects.filter(user=user):
            BlacklistedToken.objects.get_or_create(token=token)
