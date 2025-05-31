from apps.core.api.serializers import ModelBaseSerializer
from apps.users.api.serializers import UserSerializer

from ... import models


class AssignmentSerializer(ModelBaseSerializer):
    """Serializer for Assignment model."""

    creator_data = UserSerializer(
        source="creator",
        read_only=True,
    )

    class Meta:
        model = models.Assignment
        fields = (
            "id",
            "creator_data",
            "title",
            "description",
            "start",
            "deadline",
            "created",
            "modified",
        )
