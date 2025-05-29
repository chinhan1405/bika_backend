from rest_framework.permissions import IsAuthenticated

from apps.core.api.views import ReadOnlyViewSet

from ... import models
from .. import serializers


class UsersViewSet(ReadOnlyViewSet):
    """ViewSet for viewing accounts."""

    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    base_permission_classes = (
        IsAuthenticated,
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
    )
    ordering_fields = (
        "first_name",
        "last_name",
        "email",
    )
