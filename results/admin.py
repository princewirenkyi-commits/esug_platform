from django.contrib import admin
from .models import QuizAttempt, Answer, Recommendation

# Register your models here.

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ["question", "selected_option", "is_correct"]
 
 
@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ["student", "quiz", "score", "passed", "status", "submitted_at"]
    list_filter = ["passed", "status", "quiz__course__department"]
    search_fields = ["student__email", "quiz__title"]
    readonly_fields = ["score", "earned_marks", "total_marks", "passed"]
    inlines = [AnswerInline]
 
 
@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ["attempt", "generated_at"]
    readonly_fields = ["attempt", "overall_feedback", "strengths",
                       "weaknesses", "study_plan", "resources_suggested"]

