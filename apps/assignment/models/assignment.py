from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Assignment(BaseModel):
    """Implement your model here."""

    creator = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="assignments",
        verbose_name=_("Creator"),
        null=True,
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("Title"),
    )
    description = models.TextField(
        verbose_name=_("Description"),
    )
    start = models.DateTimeField(
        verbose_name=_("Start time"),
        null=True,
        blank=True,
    )
    deadline = models.DateTimeField(
        verbose_name=_("Deadline"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Assignment")
        verbose_name_plural = _("Assignments")

    def __str__(self) -> str:
        return self.title
