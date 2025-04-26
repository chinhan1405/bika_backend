from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AssignmentAppConfig(AppConfig):
    """Default configuration for Assignment app."""

    name = "apps.assignment"
    verbose_name = _("Assignment")
