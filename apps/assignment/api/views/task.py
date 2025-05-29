from decimal import Decimal

from django.db import models

from rest_framework import decorators, mixins, response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from apps.core.api.mixins import UpdateModelWithoutPatchMixin
from apps.core.api.views import BaseViewSet

from ... import constants, filters
from ... import models as assignment_model
from .. import serializers


class TaskViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    UpdateModelWithoutPatchMixin,
    BaseViewSet,
):
    """Api viewset for Task model."""

    queryset = assignment_model.Task.objects.all()
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

    @extend_schema(
        responses={
            200: serializers.TaskCompletedPercentSerializer(),
        },
    )
    @decorators.action(
        detail=False,
        methods=["GET"],
        url_path="percent-completed",
        url_name="percent_completed",
    )
    def get_percent_completed(
        self,
        request,
        *args,
        **kwargs,
    ) -> response.Response:
        """Get percent completed for all tasks."""
        queryset: models.BaseManager[assignment_model.Task] = (
            self.get_queryset()
        )
        serializer = serializers.TaskCompletedPercentSerializer(
            {
                "percent_completed": Decimal(
                    sum(
                        1 for task in queryset
                        if task.status == constants.TaskStatus.COMPLETED
                    )
                    / (
                        sum(
                            1 for task in queryset
                            if task.status in (
                                constants.TaskStatus.COMPLETED,
                                constants.TaskStatus.IN_PROGRESS,
                                constants.TaskStatus.READY_FOR_REVIEW,
                            )
                        ) or 1
                    ),
                ),
            },
        )
        return response.Response(serializer.data)
