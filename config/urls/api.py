from django.urls import include, path

import apps.assignment.api.urls

app_name = "api"


urlpatterns = [
    # API urls
    path("users/", include("apps.users.api.urls")),
    path("auth/", include("apps.auth.api.urls")),
    *apps.assignment.api.urls.urlpatterns,
]
