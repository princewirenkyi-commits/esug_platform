
from rest_framework import serializers
from .models import Course, VideoResource
 
 
class VideoResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoResource
        fields = [
            "id", "title", "url", "platform",
            "description", "duration_minutes", "created_at",
        ]
        read_only_fields = ["id", "created_at"]
 
 
class CourseSerializer(serializers.ModelSerializer):
    department_code = serializers.CharField(source="department.code", read_only=True)
    level_number = serializers.IntegerField(source="level.number", read_only=True)
    video_resources = VideoResourceSerializer(many=True, read_only=True)
    quiz_count = serializers.SerializerMethodField()
 
    class Meta:
        model = Course
        fields = [
            "id", "name", "code", "description",
            "department", "department_code",
            "level", "level_number",
            "is_general", "credit_hours",
            "video_resources", "quiz_count",
        ]
 
    def get_quiz_count(self, obj):
        return obj.quizzes.count()

