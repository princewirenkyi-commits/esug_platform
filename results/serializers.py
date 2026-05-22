
from rest_framework import serializers
from .models import QuizAttempt, Answer, Recommendation
 
 
class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = [
            "id", "overall_feedback", "strengths", "weaknesses",
            "study_plan", "resources_suggested", "generated_at",
        ]
 
 
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "question", "selected_option", "is_correct"]
 
 
class QuizAttemptSerializer(serializers.ModelSerializer):
    recommendation = RecommendationSerializer(read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)
    quiz_title = serializers.CharField(source="quiz.title", read_only=True)
    course_name = serializers.CharField(source="quiz.course.name", read_only=True)
 
    class Meta:
        model = QuizAttempt
        fields = [
            "id", "quiz", "quiz_title", "course_name", "status",
            "score", "total_marks", "earned_marks", "passed",
            "started_at", "submitted_at", "answers", "recommendation",
        ]
        read_only_fields = [
            "id", "status", "score", "total_marks",
            "earned_marks", "passed", "started_at", "submitted_at",
        ]