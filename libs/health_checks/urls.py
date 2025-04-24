from django.urls import path

from libs.health_checks import views

app_name = "libs.health_checks"

urlpatterns = [
    # Django Health Check url
    # See more details: https://pypi.org/project/django-health-check/
    # Use custom view and checkers from `libs/health_check/backends`
    path(
        "healthz/",
        views.health_check_view,
        name="health_check_home",
    ),
    path(
        "healthz/<str:subset>/",
        views.health_check_view,
        name="health_check_subset",
    ),
    path(
        "livez/",
        views.liveness_check,
        name="livez",
    ),
    path(
        "readyz/",
        views.liveness_check,
        name="readyz",
    ),
]
