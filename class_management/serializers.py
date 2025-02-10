# User Serializer
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User
from .models import SemesterSchedule, Department, Course, Attendance, Task, Notification, AcademicCalendar

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role','is_active', 'phone']
        extra_kwargs = {'password': {'write_only': True}}
    def validate_password(self, value):
        if len(value) < 8 or len(value) > 16:
            raise serializers.ValidationError("Password must be between 8 and 16 characters.")
        return value
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
             phone=validated_data.get('phone', '')

        )
        return user
    def update(self, instance, validated_data):
        if 'password' in validated_data:
             instance.password = make_password(validated_data['password'])
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

# Course Serializer
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','name','course_code','year','semester','teacher','department', 'isActive']


# Attendance Serializer
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

# Task Serializer
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

# Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
class LoginSerializer(serializers.Serializer):
   email = serializers.CharField()
   password = serializers.CharField(write_only=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
         if data['new_password'] != data['confirm_password']:
           raise serializers.ValidationError("Passwords must match")
         if len(data['new_password']) < 8 or len(data['new_password']) > 16:
           raise serializers.ValidationError("Password must be between 8 and 16 characters.")

         return data
class CreateRegistrarSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField()
def validate_period(value):
    if not isinstance(value, int):
        raise serializers.ValidationError("Period must be an integer.")
    if not 1 <= value <= 8:
        raise serializers.ValidationError("Period must be an integer between 1 and 8.")

class SemesterScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterSchedule
        fields = ['id', 'course', 'subject', 'teacher', 'section', 'day_of_week', 'period', 'details', 'semester', 'department', 'classroom_number', 'start_time', 'end_time']
        
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
class RoleSerializer(serializers.Serializer):
    roles = serializers.ListField(child=serializers.CharField())
# Course Serializer

from .models import Section
class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'
class AcademicCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicCalendar
        fields = '__all__'
class PasswordResetRequestSerializer(serializers.Serializer):
  email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
  token = serializers.CharField()
  new_password = serializers.CharField(write_only=True)
  confirm_password = serializers.CharField(write_only=True)

  def validate(self, data):
    if data['new_password'] != data['confirm_password']:
        raise serializers.ValidationError("Passwords must match")
    if len(data['new_password']) < 8 or len(data['new_password']) > 16:
           raise serializers.ValidationError("Password must be between 8 and 16 characters.")
    return data
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
###########################################################################################
