from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
 
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["email", "username", "full_name", "department", "level", "is_staff"]
    list_filter = ["department", "level", "is_staff", "is_active"]
    search_fields = ["email", "username", "first_name", "last_name", "student_id"]
    ordering = ["email"]
 
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Student Info", {
            "fields": ("student_id", "department", "level", "bio", "avatar", "date_of_birth"),
        }),
    )

