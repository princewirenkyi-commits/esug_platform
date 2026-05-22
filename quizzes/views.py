from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Quiz, Question, Option
from .serializers import QuizSerializer, QuizDetailSerializer
from .ai_generator import generate_quiz_with_ai
from courses.models import Course

# Create your views here.

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.select_related("course").prefetch_related(
        "questions__options"
    )
    serializer_class = QuizSerializer
 
    def get_serializer_class(self):
        if self.action == "retrieve":
            return QuizDetailSerializer
        return QuizSerializer
 
    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy", "generate"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]
 
    @action(detail=False, methods=["post"], permission_classes=[IsAdminUser])
    def generate(self, request):
        """
        POST /api/quizzes/generate/
        Body: { course_id, difficulty, num_questions }
        Triggers AI to generate and save a quiz.
        """
        course_id = request.data.get("course_id")
        difficulty = request.data.get("difficulty", "medium")
        num_questions = int(request.data.get("num_questions", 10))
 
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(
                {"detail": "Course not found."},
                status=status.HTTP_404_NOT_FOUND
            )
 
        try:
            quiz = generate_quiz_with_ai(course, difficulty, num_questions)
            return Response(
                QuizDetailSerializer(quiz).data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"detail": f"AI generation failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


