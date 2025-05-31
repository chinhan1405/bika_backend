from django.contrib import admin

from apps.core.admin import BaseAdmin

from .. import models


@admin.register(models.Task)
class TaskAdmin(BaseAdmin):
    """Admin UI for Task model."""

    ordering = (
        "-id",
    )
    list_display = (
        "id",
        "title",
        "status",
        "start",
        "end",
        "created",
    )
    list_display_links = (
        "title",
    )
    list_filter = (
        "status",
    )
    search_fields = (
        "title",
        "description",
        "assignment__title",
    )
    fieldsets = (
        (
            None, {
                "fields": (
                    "assignment",
                    "assignee",
                    "creator",
                    "title",
                    "description",
                    "status",
                    "start",
                    "end",
                ),
            },
        ),
    )
