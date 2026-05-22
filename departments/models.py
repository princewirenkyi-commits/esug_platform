from django.db import models

# Create your models here.
  
class Department(models.Model):
    """
    Represents an engineering department.
    Pre-populated with: BMEN, CPEN, AREN, FPEN, MTEN
    """
    CODE_CHOICES = [
        ("BMEN", "Biomedical Engineering"),
        ("CPEN", "Computer Engineering"),
        ("AREN", "Agricultural Engineering"),
        ("FPEN", "Food Process Engineering"),
        ("MTEN", "Material Science and Engineering"),
    ]
 
    code = models.CharField(max_length=8, unique=True, choices=CODE_CHOICES)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    created_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ["code"]
        verbose_name = "Department"
        verbose_name_plural = "Departments"
 
    def __str__(self):
        return f"{self.code} — {self.name}"
 
 
class Level(models.Model):
    """
    Academic year level. Fixed: 100, 200, 300, 400.
    """
    LEVEL_CHOICES = [
        (100, "Level 100"),
        (200, "Level 200"),
        (300, "Level 300"),
        (400, "Level 400"),
    ]
 
    number = models.IntegerField(unique=True, choices=LEVEL_CHOICES)
 
    class Meta:
        ordering = ["number"]
 
    def __str__(self):
        return f"Level {self.number}"


