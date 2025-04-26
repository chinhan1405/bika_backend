from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from apps.core.api.mixins import UpdateModelWithoutPatchMixin
from apps.core.api.views import BaseViewSet

from ... import filters, models
from .. import serializers


class TaskViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    UpdateModelWithoutPatchMixin,
    mixins.DestroyModelMixin,
    BaseViewSet,
):
    """Api viewset for Task model."""

    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    base_permission_classes = (
        IsAuthenticated,
    )
    search_fields = (
        "title",
        "assignment__title",
        "assignee__email",
    )
    ordering_fields = (
        "start",
        "end",
        "created",
    )
    filterset_class = filters.TaskFilter
