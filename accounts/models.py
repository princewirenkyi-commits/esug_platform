from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Students and admins both use this model.
    """
    email = models.EmailField(unique=True)
    student_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )
    level = models.ForeignKey(
        "departments.Level",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True, default="")
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
 
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]
 
    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = "User"
        verbose_name_plural = "Users"
 
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
 
    @property
    def full_name(self):
        return self.get_full_name()
