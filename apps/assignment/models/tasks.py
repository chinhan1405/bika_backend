from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel

from ..constants import TaskStatus


class Task(BaseModel):
    """Implement your model here."""

    assignment = models.ForeignKey(
        "assignment.Assignment",
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name=_("Assignment"),
    )
    assignee = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="tasks",
        verbose_name=_("Assignee"),
        null=True,
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("Title"),
    )
    description = models.TextField(
        verbose_name=_("Description"),
    )
    status = models.CharField(
        max_length=20,
        verbose_name=_("Status"),
        choices=TaskStatus.choices,
        default=TaskStatus.BACKLOG,
    )
    start = models.DateTimeField(
        verbose_name=_("Start date"),
        null=True,
        blank=True,
    )
    end = models.DateTimeField(
        verbose_name=_("End date"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
