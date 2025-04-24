from django.contrib import admin
from django.urls import include, path

from apps.core.views import IndexView

from .api_versions import urlpatterns as api_urlpatterns
from .debug import urlpatterns as debug_urlpatterns

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("mission-control-center/", admin.site.urls),
    path("", include("libs.health_checks.urls", namespace="healthz")),
]

urlpatterns += api_urlpatterns
urlpatterns += debug_urlpatterns
