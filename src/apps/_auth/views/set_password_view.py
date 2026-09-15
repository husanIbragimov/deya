from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps._auth.serializers.set_password_serializer import SetPasswordSerializer
from apps._auth.services.auth_service import AuthService
from apps.common.base_api import BaseGenericAPI


@extend_schema(tags=["User"])
class SetPasswordAPIView(BaseGenericAPI):
    """
    Lets an authenticated user set a new password for themselves without knowing the old
    one. Logs the user out of every existing session by blacklisting their refresh tokens.
    """

    serializer_class = SetPasswordSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        AuthService.set_password(request.user, self.validate_data["password"])
        return Response(status=status.HTTP_205_RESET_CONTENT)
