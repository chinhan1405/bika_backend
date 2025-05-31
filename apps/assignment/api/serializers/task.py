from rest_framework import serializers

from apps.core.api.serializers import ModelBaseSerializer
from apps.users.api.serializers import UserSerializer

from ... import models
from .assignment import AssignmentSerializer


class TaskSerializer(ModelBaseSerializer):
    """Serializer for Task model."""

    assignment_data = AssignmentSerializer(
        source="assignment",
        read_only=True,
    )
    creator_data = UserSerializer(
        source="creator",
        read_only=True,
    )
    assignee_data = UserSerializer(
        source="assignee",
        read_only=True,
    )

    class Meta:
        model = models.Task
        fields = (
            "id",
            "assignment",
            "assignment_data",
            "creator_data",
            "assignee",
            "assignee_data",
            "title",
            "description",
            "status",
            "start",
            "end",
            "created",
            "modified",
        )


class TaskCompletedPercentSerializer(serializers.Serializer):
    """Serializer for representing percent completed for Task model."""

    percent_completed = serializers.IntegerField(
        read_only=True,
    )
