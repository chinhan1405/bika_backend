from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"assignments", views.AssignmentViewSet)
router.register(r"tasks", views.TaskViewSet)
urlpatterns = router.urls
