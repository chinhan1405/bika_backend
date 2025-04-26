from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"assignment", views.AssignmentViewSet)
router.register(r"task", views.TaskViewSet)
urlpatterns = router.urls
