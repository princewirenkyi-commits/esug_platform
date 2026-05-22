from django.db import models
from courses.models import Course

# Create your models here.
 
 
class Quiz(models.Model):
    """
    A quiz is tied to a specific course.
    The AI generates questions. Each quiz has a title, difficulty, and question set.
    """
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]
 
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="quizzes"
    )
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, default="")
    difficulty = models.CharField(
        max_length=10, choices=DIFFICULTY_CHOICES, default="medium"
    )
    time_limit_minutes = models.PositiveIntegerField(default=30)
    pass_mark_percent = models.PositiveSmallIntegerField(default=50)
    is_ai_generated = models.BooleanField(default=True)
    ai_prompt_used = models.TextField(blank=True, help_text="Prompt sent to AI to generate this quiz")
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"
 
    def __str__(self):
        return f"{self.title} [{self.course.name}]"
 
    @property
    def question_count(self):
        return self.questions.count()
 
 
class Question(models.Model):
    """Multiple-choice question belonging to a quiz."""
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="questions"
    )
    text = models.TextField()
    explanation = models.TextField(
        blank=True, help_text="Shown after quiz submission"
    )
    order = models.PositiveSmallIntegerField(default=0)
    marks = models.PositiveSmallIntegerField(default=1)
 
    class Meta:
        ordering = ["order"]
 
    def __str__(self):
        return f"Q{self.order}: {self.text[:60]}..."
 
 
class Option(models.Model):
    """An answer option for a multiple-choice question."""
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="options"
    )
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
 
    def __str__(self):
        return f"[correct={self.is_correct}] {self.text[:60]}"
