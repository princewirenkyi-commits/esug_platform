
# quizzes/urls.py
from rest_framework.routers import DefaultRouter
from . import views
 
router = DefaultRouter()
router.register("", views.QuizViewSet, basename="quiz")
 
urlpatterns = router.urls

