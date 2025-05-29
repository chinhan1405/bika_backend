from apps.core.api.serializers import ModelBaseSerializer
from apps.users.api.serializers import UserSerializer

from ... import models


class AssignmentSerializer(ModelBaseSerializer):
    """Serializer for Assignment model."""

    creator_data = UserSerializer(
        source="creator",
        read_only=True,
    )

    def validate(self, attrs: dict) -> dict:
        """Automatically set the creator to the current user."""
        validated_data = super().validate(attrs)
        if not validated_data.get("creator"):
            validated_data["creator"] = self._user
        return validated_data

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
