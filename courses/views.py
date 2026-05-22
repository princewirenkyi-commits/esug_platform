from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course, VideoResource
from .serializers import CourseSerializer, VideoResourceSerializer

# Create your views here.


 
 
class CourseViewSet(viewsets.ModelViewSet):
    """
    GET  /api/courses/          — List courses (filterable by level, department)
    POST /api/courses/          — Admin only: Create a course (Level 200-400)
    GET  /api/courses/{id}/     — Retrieve a single course with video resources
    PUT  /api/courses/{id}/     — Admin only: Update course
    DELETE /api/courses/{id}/   — Admin only: Delete course
    """
    queryset = Course.objects.select_related("department", "level").prefetch_related("video_resources")
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["level__number", "department__code", "is_general"]
    search_fields = ["name", "code", "description"]
 
    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]
 
 
class VideoResourceViewSet(viewsets.ModelViewSet):
    queryset = VideoResource.objects.select_related("course")
    serializer_class = VideoResourceSerializer
 
    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]
 
    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)
