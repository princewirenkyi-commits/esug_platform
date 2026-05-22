from django.core.management.base import BaseCommand
from departments.models import Department, Level
from courses.models import Course
 
 
GENERAL_COURSES = [
    {"name": "Calculus 1", "code": "MATH101", "credit_hours": 3},
    {"name": "Statics for Mechanics", "code": "MECH101", "credit_hours": 3},
    {"name": "Introduction to Engineering", "code": "ENGR101", "credit_hours": 2},
    {"name": "General Physics", "code": "PHYS101", "credit_hours": 3},
]
 
CPEN_ONLY = [
    {"name": "Computer Innovations", "code": "CPEN101", "credit_hours": 3},
]
 
NON_CPEN_ONLY = [
    {"name": "Chemistry", "code": "CHEM101", "credit_hours": 3},
]
 
 
class Command(BaseCommand):
    help = "Seed Level 100 courses for all departments"
 
    def handle(self, *args, **kwargs):
        level_100, _ = Level.objects.get_or_create(number=100)
        self.stdout.write("Seeding Level 100 courses...")
 
        # Create Level objects for 200, 300, 400 too
        for num in [200, 300, 400]:
            Level.objects.get_or_create(number=num)
 
        # Create departments
        dept_data = [
            ("BMEN", "Biomedical Engineering"),
            ("CPEN", "Computer Engineering"),
            ("AREN", "Agricultural Engineering"),
            ("FPEN", "Food Process Engineering"),
            ("MTEN", "Materials Engineering"),
        ]
        for code, name in dept_data:
            Department.objects.get_or_create(code=code, defaults={"name": name})
 
        # Seed general courses (all departments)
        for course_data in GENERAL_COURSES:
            obj, created = Course.objects.get_or_create(
                code=course_data["code"],
                defaults={
                    **course_data,
                    "level": level_100,
                    "is_general": True,
                    "is_seeded": True,
                    "department": None,
                }
            )
            status = "created" if created else "exists"
            self.stdout.write(f"  {course_data['name']} — {status}")
 
        # Chemistry for all except CPEN
        non_cpen_depts = Department.objects.exclude(code="CPEN")
        for dept in non_cpen_depts:
            for course_data in NON_CPEN_ONLY:
                code = f"{course_data['code']}_{dept.code}"
                obj, created = Course.objects.get_or_create(
                    code=code,
                    defaults={
                        **course_data,
                        "code": code,
                        "level": level_100,
                        "is_seeded": True,
                        "department": dept,
                    }
                )
                self.stdout.write(f"  {course_data['name']} ({dept.code}) — {'created' if created else 'exists'}")
 
        # CPEN-only courses
        cpen = Department.objects.get(code="CPEN")
        for course_data in CPEN_ONLY:
            obj, created = Course.objects.get_or_create(
                code=course_data["code"],
                defaults={
                    **course_data,
                    "level": level_100,
                    "is_seeded": True,
                    "department": cpen,
                }
            )
            self.stdout.write(f"  {course_data['name']} (CPEN) — {'created' if created else 'exists'}")
 
        self.stdout.write(self.style.SUCCESS("Level 100 seeding complete!"))

