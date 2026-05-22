from django.db import models
from django.conf import settings
from quizzes.models import Quiz, Question, Option
 

# Create your models here.


class QuizAttempt(models.Model):
    """
    Records a student's complete attempt at a quiz.
    One student can attempt a quiz multiple times.
    """
    STATUS_CHOICES = [
        ("in_progress", "In Progress"),
        ("submitted", "Submitted"),
        ("analysed", "Analysed"),
    ]
 
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_attempts",
    )
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="attempts"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="in_progress")
    score = models.FloatField(null=True, blank=True, help_text="Percentage score")
    total_marks = models.PositiveIntegerField(default=0)
    earned_marks = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
 
    class Meta:
        ordering = ["-started_at"]
 
    def __str__(self):
        return f"{self.student.email} — {self.quiz.title} ({self.score}%)"
 
    def calculate_score(self):
        """Compute score from answers, save, and mark passed/failed."""
        answers = self.answers.select_related("selected_option")
        total = sum(a.question.marks for a in answers)
        earned = sum(
            a.question.marks
            for a in answers
            if a.selected_option and a.selected_option.is_correct
        )
        self.total_marks = total
        self.earned_marks = earned
        self.score = round((earned / total * 100), 2) if total > 0 else 0
        self.passed = self.score >= self.quiz.pass_mark_percent
        self.status = "submitted"
        self.save()
        return self.score
 
 
class Answer(models.Model):
    """Individual answer to one question within an attempt."""
    attempt = models.ForeignKey(
        QuizAttempt, on_delete=models.CASCADE, related_name="answers"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE
    )
    selected_option = models.ForeignKey(
        Option, on_delete=models.SET_NULL, null=True, blank=True
    )
    is_correct = models.BooleanField(null=True, blank=True)
 
    class Meta:
        unique_together = ["attempt", "question"]
 
 
class Recommendation(models.Model):
    """
    AI-generated study recommendation per quiz attempt.
    Generated after quiz submission by calling Anthropic API.
    """
    attempt = models.OneToOneField(
        QuizAttempt, on_delete=models.CASCADE, related_name="recommendation"
    )
    overall_feedback = models.TextField()
    strengths = models.TextField()
    weaknesses = models.TextField()
    study_plan = models.TextField()
    resources_suggested = models.TextField()
    ai_raw_response = models.TextField(blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f"Recommendation for {self.attempt}"
