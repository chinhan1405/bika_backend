from django.utils.translation import gettext_lazy as _

from rest_framework import mixins, response, status
from rest_framework.permissions import IsAuthenticated

from apps.core.api.mixins import UpdateModelWithoutPatchMixin
from apps.core.api.views import BaseViewSet
from apps.users.permissions import IsAdmin, IsLecturer

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

    queryset = models.Assignment.objects.all().select_related(
        "creator",
    )
    serializer_class = serializers.AssignmentSerializer
    base_permission_classes = (
        IsAuthenticated,
    )
    extra_permissions_map = {
        "create": (IsLecturer | IsAdmin,),
        "update": (IsLecturer | IsAdmin,),
        "delete": (IsLecturer | IsAdmin,),
    }
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

    def create(self, request, *args, **kwargs):
        """Create a new assignment."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["creator"] = request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return self.response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def destroy(self, request, *args, **kwargs):
        """Delete an assignment."""
        instance: models.Assignment = self.get_object()
        if instance.creator != request.user:
            return response.Response(
                {
                    "detail": _(
                        "You do not have permission "
                        "to delete this assignment.",
                    ),
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)
