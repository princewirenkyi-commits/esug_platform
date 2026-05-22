
from rest_framework import serializers
from .models import Department, Level
 
 
class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ["id", "number"]
 
 
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "code", "name", "description", "icon"]

