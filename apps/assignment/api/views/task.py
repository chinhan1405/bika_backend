from decimal import Decimal

from django.db import models

from rest_framework import decorators, mixins, response, status
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
    mixins.DestroyModelMixin,
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

    def create(self, request, *args, **kwargs) -> response.Response:
        """Create a new task."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["creator"] = request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def destroy(self, request, *args, **kwargs) -> response.Response:
        """Delete a task."""
        instance: assignment_model.Task = self.get_object()
        if instance.creator != request.user:
            return response.Response(
                {"detail": "You do not have permission to delete this task."},
                status=status.HTTP_403_FORBIDDEN,
            )
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)


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
                ) * 100,
            },
        )
        return response.Response(serializer.data)
