from django.contrib import admin

from apps.core.admin import BaseAdmin

from .. import models


@admin.register(models.Assignment)
class AssignmentAdmin(BaseAdmin):
    """Admin UI for Assignment model."""

    ordering = (
        "-id",
    )
    list_display = (
        "id",
        "title",
        "creator",
        "start",
        "deadline",
        "created",
    )
    list_display_links = (
        "title",
    )
    search_fields = (
        "title",
        "description",
    )
    fieldsets = (
        (
            None, {
                "fields": (
                    "creator",
                    "title",
                    "description",
                    "start",
                    "deadline",
                ),
            },
        ),
    )
