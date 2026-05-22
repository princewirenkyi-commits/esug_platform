from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import QuizAttempt, Answer, Recommendation
from .serializers import (
    QuizAttemptSerializer, RecommendationSerializer
)
from .analyzer import generate_recommendation

# Create your views here.

 
class QuizAttemptViewSet(viewsets.ModelViewSet):
    """
    POST /api/results/attempts/           — Start a new quiz attempt
    POST /api/results/attempts/{id}/submit/ — Submit answers
    GET  /api/results/attempts/{id}/recommendation/ — Get AI recommendation
    GET  /api/results/attempts/           — List own attempts
    """
    permission_classes = [IsAuthenticated]
    serializer_class = QuizAttemptSerializer
 
    def get_queryset(self):
        return QuizAttempt.objects.filter(
            student=self.request.user
        ).select_related("quiz__course", "recommendation")
 
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
 
    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        """
        Accepts list of {question_id, option_id} pairs.
        Saves answers, calculates score, triggers AI recommendation.
        """
        attempt = self.get_object()
        if attempt.status != "in_progress":
            return Response(
                {"detail": "This attempt has already been submitted."},
                status=status.HTTP_400_BAD_REQUEST,
            )
 
        answers_data = request.data.get("answers", [])
        for ans in answers_data:
            Answer.objects.update_or_create(
                attempt=attempt,
                question_id=ans["question_id"],
                defaults={"selected_option_id": ans.get("option_id")},
            )
 
        attempt.submitted_at = timezone.now()
        attempt.calculate_score()
 
        # Async-friendly: call AI recommendation
        try:
            generate_recommendation(attempt)
        except Exception as e:
            # Log error but don't fail the submission
            print(f"Recommendation generation failed: {e}")
 
        return Response(
            QuizAttemptSerializer(attempt).data,
            status=status.HTTP_200_OK,
        )
 
    @action(detail=True, methods=["get"])
    def recommendation(self, request, pk=None):
        """GET /api/results/attempts/{id}/recommendation/"""
        attempt = self.get_object()
        try:
            rec = attempt.recommendation
            return Response(RecommendationSerializer(rec).data)
        except Recommendation.DoesNotExist:
            return Response(
                {"detail": "Recommendation not yet generated."},
                status=status.HTTP_404_NOT_FOUND,
            )