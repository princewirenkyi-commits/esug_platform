
from rest_framework import serializers
from .models import Quiz, Question, Option
 
 
class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "text"]  # is_correct hidden during quiz
 
 
class OptionDetailSerializer(serializers.ModelSerializer):
    """Used in admin/results context — exposes is_correct."""
    class Meta:
        model = Option
        fields = ["id", "text", "is_correct"]
 
 
class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
 
    class Meta:
        model = Question
        fields = ["id", "text", "order", "marks", "options"]
 
 
class QuizSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.name", read_only=True)
    question_count = serializers.IntegerField(read_only=True)
 
    class Meta:
        model = Quiz
        fields = [
            "id", "title", "description", "difficulty",
            "time_limit_minutes", "pass_mark_percent",
            "is_ai_generated", "is_published",
            "course", "course_name", "question_count", "created_at",
        ]
 
 
class QuizDetailSerializer(QuizSerializer):
    """Full quiz with all questions and options. Used on retrieve."""
    questions = QuestionSerializer(many=True, read_only=True)
 
    class Meta(QuizSerializer.Meta):
        fields = QuizSerializer.Meta.fields + ["questions"]

