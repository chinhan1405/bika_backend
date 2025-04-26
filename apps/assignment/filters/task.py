from django_filters import rest_framework as filters

from .. import models


class TaskFilter(filters.FilterSet):
    """Provide filters for `Task` API."""

    class Meta:
        model = models.Task
        fields = (
            "assignee_id",
            "assignment_id",
            "status",
        )
