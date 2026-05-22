
from rest_framework.routers import DefaultRouter
from . import views
 
router = DefaultRouter()
router.register("departments", views.DepartmentViewSet)
router.register("levels", views.LevelViewSet)
 
urlpatterns = router.urls
