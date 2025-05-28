from django.contrib.auth import login, user_logged_in
from django.utils.translation import gettext_lazy as _

from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from knox.views import LoginView as KnoxLoginView

from . import serializers


class LoginView(KnoxLoginView):
    """User authentication view.

    We're using custom one because Knox using basic auth as default
    authorization method.

    """

    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        """Login user and get auth token with expiry."""
        serializer = serializers.AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(request, serializer.validated_data["user"]) # type: ignore
        return super().post(request, format=None)


class SignupView(KnoxLoginView):
    """User registration view.

    We're using custom one because Knox using basic auth as default
    authorization method.

    """

    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs) -> Response:
        """Register user and get auth token with expiry."""
        serializer = serializers.SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        guest = serializer.save()
        login(request, guest)
        instance, token = self.create_token()
        user_logged_in.send(
            sender=request.user.__class__,
            request=request,
            user=request.user,
        )
        return self.get_post_response(request, token, instance)


class PasswordResetView(GenericAPIView):
    """Change user's password on reset.

    If email is valid, simply sends password with link that leads to frontend
    with token need for reset.

    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        """Request password reset.

        Warning: it will always return `Password reset e-mail has been sent.`

        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(GenericAPIView):
    """Complete password reset workflow.

    This endpoint confirms the reset of user's password.

    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        """Complete password reset."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": _("Password has been reset with the new password.")},
            status=status.HTTP_200_OK,
        )

class ChangePasswordView(GenericAPIView):
    """Change password for current user."""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        """Change password for current user."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": _("Password has been changed to the new password.")},
            status=status.HTTP_200_OK,
        )
