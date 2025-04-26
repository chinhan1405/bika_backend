from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from apps.core.api.mixins import UpdateModelWithoutPatchMixin
from apps.core.api.views import BaseViewSet

from ... import filters, models
from .. import serializers


class AssignmentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    UpdateModelWithoutPatchMixin,
    mixins.DestroyModelMixin,
    BaseViewSet,
):
    """Api viewset for Assignment model."""

    queryset = models.Assignment.objects.all()
    serializer_class = serializers.AssignmentSerializer
    base_permission_classes = (
        IsAuthenticated,
    )
    search_fields = (
        "title",
        "creator__email",
    )
    ordering_fields = (
        "start",
        "deadline",
        "created",
    )
    filterset_class = filters.AssignmentFilter
