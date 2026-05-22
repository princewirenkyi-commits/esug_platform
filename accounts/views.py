from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserProfileSerializer

# Create your views here.
 
User = get_user_model()
 
 
class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/ — Public endpoint for new user signup."""
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserProfileSerializer(user).data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
        }, status=status.HTTP_201_CREATED)
 
 
class LogoutView(APIView):
    """POST /api/auth/logout/ — Blacklists the refresh token."""
    permission_classes = [IsAuthenticated]
 
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logged out successfully."})
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
 
 
class ProfileView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/auth/profile/ — Retrieve or update own profile."""
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
 
    def get_object(self):
        return self.request.user

