from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Department, Level
from .serializers import DepartmentSerializer, LevelSerializer

# Create your views here.
 
class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    """List all departments. Read-only for all authenticated users."""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
 
 
class LevelViewSet(viewsets.ReadOnlyModelViewSet):
    """List all levels (100, 200, 300, 400)."""
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes = [IsAuthenticated]
