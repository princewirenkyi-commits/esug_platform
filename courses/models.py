from django.db import models
from departments.models import Department, Level


# Create your models here.

class Course(models.Model):
    """
    A course belongs to one or more departments and a specific level.
    Level 100 courses are seeded via management command.
    Level 200-400 courses are admin-managed.
    """
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, default="")
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="courses",
        null=True,
        blank=True,
        help_text="Null means the course is for ALL departments.",
    )
    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        related_name="courses",
    )
    is_general = models.BooleanField(
        default=False,
        help_text="True if course applies to all departments.",
    )
    is_seeded = models.BooleanField(
        default=False,
        help_text="True if course was auto-created by seed_level100 command.",
    )
    credit_hours = models.PositiveSmallIntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering = ["level__number", "name"]
        verbose_name = "Course"
        verbose_name_plural = "Courses"
 
    def __str__(self):
        dept = self.department.code if self.department else "ALL"
        return f"[{dept}] {self.name} (Level {self.level.number})"
 
 
class VideoResource(models.Model):
    """A curated video link associated with a specific course."""
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="video_resources"
    )
    title = models.CharField(max_length=300)
    url = models.URLField()
    platform = models.CharField(
        max_length=50,
        choices=[
            ("youtube", "YouTube"),
            ("vimeo", "Vimeo"),
            ("other", "Other"),
        ],
        default="youtube",
    )
    description = models.TextField(blank=True, default="")
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    added_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="added_videos",
    )
    created_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ["-created_at"]
 
    def __str__(self):
        return f"{self.title} ({self.course.name})"

