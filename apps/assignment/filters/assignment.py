from django_filters import rest_framework as filters

from .. import models


class AssignmentFilter(filters.FilterSet):
    """Provide filters for `Assignment` API."""

    class Meta:
        model = models.Assignment
        fields = ("creator_id",)
