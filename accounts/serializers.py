
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
 
User = get_user_model()
 
 
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
 
    class Meta:
        model = User
        fields = [
            "id", "email", "username", "first_name", "last_name",
            "student_id", "department", "level", "password", "password2",
        ]
 
    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields did not match."}
            )
        return attrs
 
    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
 
 
class UserProfileSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(
        source="department.name", read_only=True
    )
    level_name = serializers.CharField(
        source="level.name", read_only=True
    )
    full_name = serializers.SerializerMethodField()
 
    class Meta:
        model = User
        fields = [
            "id", "email", "username", "first_name", "last_name",
            "full_name", "student_id", "department", "department_name",
            "level", "level_name", "bio", "avatar", "date_joined",
        ]
        read_only_fields = ["id", "email", "date_joined"]
 
    def get_full_name(self, obj):
        return obj.get_full_name()

