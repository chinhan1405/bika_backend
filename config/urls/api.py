from django.urls import include, path

app_name = "api"


urlpatterns = [
    # API urls
    path("users/", include("apps.users.api.urls")),
    path("auth/", include("apps.auth.api.urls")),
]
