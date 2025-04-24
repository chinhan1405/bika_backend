import dataclasses
import platform

import django
from django.conf import settings
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.views.generic import TemplateView

from libs.permissions import can_access_debug_tools
from libs.utils import get_changelog_html, get_latest_version


@dataclasses.dataclass
class Changelog:
    """Class keeping changelog data."""

    name: str
    text: str
    version: str
    swagger_api_ui: str | None
    redoc_api_ui: str | None


ARGO_CD_URL_MAPPING = {
    "development": "https://deploy.saritasa.rocks/",
    "prod": "TODO",
}
ARGO_CD_MAPPING = {
    "development": "bika-backend-dev",
    "prod": "bika-backend-prod",
}


class AppStatsMixin:
    """Add information about app to context."""

    def get_context_data(self, **kwargs):
        """Load changelog data from files."""
        context = super().get_context_data(**kwargs)
        minio_url = (
            settings.AWS_S3_ENDPOINT_URL
            if settings.ENVIRONMENT == "local"
            else None
        )
        context.update(
            show_debug_tools=can_access_debug_tools(self.request.user),
            env=settings.ENVIRONMENT,
            version=get_latest_version("CHANGELOG.md"),
            python_version=platform.python_version(),
            django_version=django.get_version(),
            app_url=settings.FRONTEND_URL,
            app_label=settings.APP_LABEL,
            argo_cd_url=ARGO_CD_URL_MAPPING.get(
                settings.ENVIRONMENT, ARGO_CD_URL_MAPPING["development"],
            ),
            argo_cd_app=ARGO_CD_MAPPING.get(
                settings.ENVIRONMENT, ARGO_CD_MAPPING["development"],
            ),
            email_ui_url=settings.EMAIL_UI_URL,
            minio_url=minio_url,
        )
        return context


class IndexView(AppStatsMixin, TemplateView):
    """Class-based view for that shows version of open_api file on main page.

    Displays the current version of the open_api specification and changelog.

    """

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        """Load changelog data from files."""
        context = super().get_context_data(**kwargs)
        open_api_ui_urls = {
            "swagger_api_ui": "open_api:swagger",
            "redoc_api_ui": "open_api:redoc",
        }

        for key in open_api_ui_urls:
            try:
                url = reverse(open_api_ui_urls[key])
            except NoReverseMatch:
                url = None
            open_api_ui_urls[key] = url

        context["changelog"] = Changelog(
            name=settings.SPECTACULAR_SETTINGS.get("TITLE"),
            text=get_changelog_html("CHANGELOG.md"),
            version=settings.SPECTACULAR_SETTINGS.get("VERSION"),
            **open_api_ui_urls,
        )
        return context
