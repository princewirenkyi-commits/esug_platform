
from rest_framework.routers import DefaultRouter
from . import views
 
router = DefaultRouter()
router.register("attempts", views.QuizAttemptViewSet, basename="attempt")
 
urlpatterns = router.urls

