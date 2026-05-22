from django.contrib import admin
from .models import Department, Level
# Register your models here.

 
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["code", "name"]
    search_fields = ["code", "name"]
 
 
@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ["number"]
