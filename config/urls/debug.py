from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

# Debug urls
urlpatterns = []

# for serving uploaded files on dev environment with django
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
    urlpatterns = [
        *urlpatterns,
        path("__debug__/", include(debug_toolbar.urls)),
    ]
