from django.db import models


class TaskStatus(models.TextChoices):
    """Task status choices."""

    BACKLOG = "backlog", "In Backlog"
    READY = "ready", "Ready"
    IN_PROGRESS = "in_progress", "In Progress"
    READY_FOR_REVIEW = "ready_for_review", "Ready for Review"
    COMPLETED = "completed", "Completed"
    CANCELED = "canceled", "Canceled"
