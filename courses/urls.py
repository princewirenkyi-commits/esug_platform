
# courses/urls.py
from rest_framework.routers import DefaultRouter
from . import views
 
router = DefaultRouter()
router.register("courses", views.CourseViewSet)
router.register("videos", views.VideoResourceViewSet)
 
urlpatterns = router.urls
