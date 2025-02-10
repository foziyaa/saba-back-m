from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, SemesterSchedule, Attendance, Notification, Task, Course,Department,AcademicCalendar,Document
from .serializers import UserSerializer, SemesterScheduleSerializer, AttendanceSerializer, NotificationSerializer, TaskSerializer, LoginSerializer,ChangePasswordSerializer,CreateRegistrarSerializer,DepartmentSerializer,RoleSerializer,AcademicCalendarSerializer, CourseSerializer #Add CourseSerializer
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer

class RegisterUserView(APIView):

   def post(self, request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
         department_id = request.data.get('department')
         try:
              department = Department.objects.get(id=department_id)
         except Department.DoesNotExist:
              return Response({'detail': f'Department with ID {department_id} not found'}, status=status.HTTP_404_NOT_FOUND)
         serializer.save(department = department)
         return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Class Schedule
class ClassScheduleView(APIView):
    def get(self, request, id):
        try:
            
            student = User.objects.get(id=id, role='student')
            schedules = SemesterSchedule.objects.filter(teacher=student)
            serializer = SemesterScheduleSerializer(schedules, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

# Attendance Management
class AttendanceView(APIView):
    def post(self, request, id):
        try:
            student = User.objects.get(id=id, role='student')
            course_id = request.data.get('course_id')
            course = Course.objects.get(id=course_id)
            status = request.data.get('status')

            attendance = Attendance.objects.create(user=student, course=course, status=status)
            serializer = AttendanceSerializer(attendance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'detail': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

# Q&A Bulletin
class QABulletinView(APIView):
    def get(self, request):
        questions = Notification.objects.filter(type='announcement')
        serializer = NotificationSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Fast-Paced Game
class FastPacedGameView(APIView):
    def get(self, request):
        game_data = {'question': 'What is 2 + 2?', 'options': ['3', '4', '5']}
        return Response(game_data)

    def post(self, request):
        answer = request.data.get('answer')
        correct_answer = '4'
        if answer == correct_answer:
            return Response({'message': 'Correct answer!'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Wrong answer!'}, status=status.HTTP_400_BAD_REQUEST)

# Task Management
class TodoListView(APIView):
    def get(self, request, id):
        tasks = Task.objects.filter(student_id=id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        request.data['student'] = id
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    def put(self, request, id, task_id):
        task = Task.objects.get(id=task_id)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, task_id):
        task = Task.objects.get(id=task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Academic Calendar
class AcademicCalendarView(APIView):
    def get(self, request):
        calendar_data = {
            'semester_start': '2025-01-01',
            'semester_end': '2025-05-30',
            'holidays': ['2025-01-10', '2025-04-10'],
        }
        return Response(calendar_data)

# Notifications
class NotificationsView(APIView):
    def get(self, request, id):
        notifications = Notification.objects.filter(user_id=id)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

# Account Management
class AccountManagementView(APIView):
    def get(self, request, id):
        try:
            student = User.objects.get(id=id)
            serializer = UserSerializer(student)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'detail': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            student = User.objects.get(id=id)
            serializer = UserSerializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            student = User.objects.get(id=id)
            student.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'detail': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
User = get_user_model()  # ✅ Get the custom user model

@method_decorator(csrf_exempt, name="dispatch")
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            
            try:
                user = User.objects.get(email=email)  # ✅ Get user by email
                authenticated_user = authenticate(request, username=user.username, password=password)  # ✅ Authenticate using username
                
                if authenticated_user:
                    login(request, authenticated_user)
                    user_serializer = UserSerializer(authenticated_user)
                    return Response(user_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            
            except User.DoesNotExist:
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ChangePasswordView(APIView):
     def post(self, request, id):
         try:
           user = User.objects.get(id=id)
           serializer = ChangePasswordSerializer(data=request.data)
           if serializer.is_valid():
                old_password = serializer.validated_data['old_password']
                new_password = serializer.validated_data['new_password']
                if check_password(old_password, user.password):
                    user.set_password(new_password)
                    user.save()
                    return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Invalid old password'}, status=status.HTTP_401_UNAUTHORIZED)
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         except User.DoesNotExist:
             return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class CreateRegistrarView(APIView):
    def get(self, request):
        registrars = User.objects.filter(role='registrar')
        serializer = UserSerializer(registrars, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateRegistrarSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            role = serializer.validated_data['role']

            user = User.objects.create_user(
                username=name,
                email=email,
                password=password,
                role=role
            )

            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateRegistrarStatus(APIView):
    permission_classes = [AllowAny] #Remove this later
    def patch(self, request, id):
        try:
            user = User.objects.get(id=id, role='registrar')
            is_active = request.data.get('is_active') # Get is_active from the request
            if is_active is not None:
                user.is_active = is_active # Use the value from request
                user.save()
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
               return Response({'detail': 'is_active field is required'}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        registrars = User.objects.filter(role='registrar')
        serializer = UserSerializer(registrars, many =True)
        return Response(serializer.data)
    def post(self, request):
          serializer = CreateRegistrarSerializer(data=request.data)
          if serializer.is_valid():
              name = serializer.validated_data['name']
              email = serializer.validated_data['email']
              password = serializer.validated_data['password']
              role = serializer.validated_data['role']
              user = User.objects.create_user(
               username=name,
                email=email,
                 password=password,
                 role=role
             )

              user_serializer = UserSerializer(user)
              return Response(user_serializer.data, status=status.HTTP_201_CREATED)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SemesterSchedule, User, Course, Section
from .serializers import SemesterScheduleSerializer


class SemesterScheduleListView(APIView):
   def get(self, request):
       schedules = SemesterSchedule.objects.all()
       serializer = SemesterScheduleSerializer(schedules, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)

   def post(self, request):
        serializer = SemesterScheduleSerializer(data=request.data)
        if serializer.is_valid():
            teacher_id = request.data.get('teacher')
            course_id = request.data.get('course') # <------ Now getting course ID
            section_id = request.data.get('section')
            try:
                teacher = User.objects.get(id=teacher_id, role='teacher')
                course = Course.objects.get(id=course_id) #  <------ Now getting course object
                section = Section.objects.get(id=section_id)
            except User.DoesNotExist:
                return Response({'detail': f'Teacher with ID {teacher_id} not found'}, status=status.HTTP_404_NOT_FOUND)
            except Course.DoesNotExist:
                return Response({'detail': f'Course with ID {course_id} not found'}, status=status.HTTP_404_NOT_FOUND)
            except Section.DoesNotExist:
                return Response({'detail': f'Section with ID {section_id} not found'}, status=status.HTTP_404_NOT_FOUND)
            # now link to save schedule, no need to check the value from here, we check on serialiser
            serializer.save(teacher=teacher, course = course, section = section,
                period = request.data.get('period'),
                day_of_week = request.data.get('day_of_week'),
                semester = request.data.get('semester'),
                 start_time = request.data.get('start_time'),
                  end_time = request.data.get('end_time'),
                classroom_number = request.data.get('classroom_number')
               )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class SemesterScheduleDetailView(APIView):
     def delete(self, request, id):
        try:
           schedule = SemesterSchedule.objects.get(id=id)
           schedule.delete()
           return Response(status=status.HTTP_204_NO_CONTENT)
        except SemesterSchedule.DoesNotExist:
             return Response({'detail': f'Schedule with ID {id} not found'}, status=status.HTTP_404_NOT_FOUND)
     def put(self, request, id):
        try:
            schedule = SemesterSchedule.objects.get(id=id)
            serializer = SemesterScheduleSerializer(schedule, data=request.data, partial = True)
            if serializer.is_valid():
                teacher_id = request.data.get('teacher')
                course_id = request.data.get('course')
                section_id = request.data.get('section')
                try:
                    teacher = User.objects.get(id=teacher_id, role='teacher')
                    course = Course.objects.get(id = course_id)
                    section = Section.objects.get(id=section_id)
                except User.DoesNotExist:
                    return Response({'detail': f'Teacher with ID {teacher_id} not found'}, status=status.HTTP_404_NOT_FOUND)
                except Course.DoesNotExist:
                    return Response({'detail': f'Course with ID {course_id} not found'}, status=status.HTTP_404_NOT_FOUND)
                except Section.DoesNotExist:
                   return Response({'detail': f'Section with ID {section_id} not found'}, status=status.HTTP_404_NOT_FOUND)
                serializer.save(teacher = teacher, subject = course.name, section = section.name,
                  period =  request.data.get('period'),
                day_of_week = request.data.get('day_of_week'),
                semester = request.data.get('semester'),
                 start_time = request.data.get('start_time'),
                  end_time = request.data.get('end_time'),
                classroom_number = request.data.get('classroom_number'))
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except SemesterSchedule.DoesNotExist:
             return Response({'detail': f'Schedule with ID {id} not found'}, status=status.HTTP_404_NOT_FOUND)
class DepartmentDetailView(APIView):
    def get(self, request, id):
        try:
            department = Department.objects.get(id=id)
            serializer = DepartmentSerializer(department)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Department.DoesNotExist:
            return Response({'detail': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        try:
            department = Department.objects.get(id=id)
            serializer = DepartmentSerializer(department, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Department.DoesNotExist:
            return Response({'detail': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)
    def put(self, request, id):
        try:
            department = Department.objects.get(id=id)
            serializer = DepartmentSerializer(department, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Department.DoesNotExist:
            return Response({'detail': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)
class DepartmentListView(APIView):
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class RoleListView(APIView):
    def get(self, request):
        roles = User.get_available_roles()
        serializer = RoleSerializer({'roles': roles})
        return Response(serializer.data, status=status.HTTP_200_OK)

class TeacherListView(APIView):
  
  def get(self, request):
        teachers = User.objects.filter(role='teacher')
        serializer = UserSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AttendanceListView(APIView):
  
  def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Attendance saved successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  def get(self, request, id=None):
         date = request.query_params.get('date')
         if id:
             try:
                 attendances = Attendance.objects.filter(user_id=id)
                 serializer = AttendanceSerializer(attendances, many=True)
                 return Response(serializer.data, status=status.HTTP_200_OK)
             except Attendance.DoesNotExist:
                return Response({'detail': f'Attendance not found for user ID {id}'}, status=status.HTTP_404_NOT_FOUND)
         elif date:
             try:
                 attendances = Attendance.objects.filter(date=date)
                 serializer = AttendanceSerializer(attendances, many=True)
                 return Response(serializer.data, status=status.HTTP_200_OK)
             except Attendance.DoesNotExist:
                  return Response({'detail': f'Attendance not found for date {date}'}, status=status.HTTP_404_NOT_FOUND)
         else:
           attendances = Attendance.objects.all()
           serializer = AttendanceSerializer(attendances, many = True)
           return Response(serializer.data, status=status.HTTP_200_OK)
class StudentAttendanceView(APIView):
    
    def post(self, request):
         serializer = AttendanceSerializer(data=request.data)
         if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Course, Department
from .serializers import CourseSerializer
from rest_framework.permissions import AllowAny
class CreateCourseView(APIView):
    permission_classes = [AllowAny]  #Allow any users
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
           department_id = request.data.get('department')
           try:
             department = Department.objects.get(id=department_id)
           except Department.DoesNotExist:
                return Response({'detail': f'Department with ID {department_id} not found'}, status=status.HTTP_404_NOT_FOUND)
           course = serializer.save(department=department)
           return Response(CourseSerializer(course).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDetailView(APIView):
    permission_classes = [AllowAny]
    def put(self, request, id):
         try:
            course = Course.objects.get(id=id)
            serializer = CourseSerializer(course, data=request.data, partial=True)
            if serializer.is_valid():
                department_id = request.data.get('department')
                try:
                   department = Department.objects.get(id=department_id)
                except Department.DoesNotExist:
                   return Response({'detail': f'Department with ID {department_id} not found'}, status=status.HTTP_404_NOT_FOUND)
                serializer.save(department=department)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         except Course.DoesNotExist:
            return Response({'detail': f'Course with ID {id} not found'}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, id):
       try:
           course = Course.objects.get(id=id)
           course.delete()
           return Response(status=status.HTTP_204_NO_CONTENT)
       except Course.DoesNotExist:
            return Response({'detail': f'Course with ID {id} not found'}, status=status.HTTP_404_NOT_FOUND)
    def patch(self, request, id):
        try:
            course = Course.objects.get(id=id)
            serializer = CourseSerializer(course, data=request.data, partial=True)
            if serializer.is_valid():
                 serializer.save()
                 return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
               return Response({'detail': f'Course with ID {id} not found'}, status=status.HTTP_404_NOT_FOUND)
from .serializers import SectionSerializer
from .models import Section
class SectionListView(APIView):


   def get(self, request, department_id = None):
     if department_id:
         try:
             department = Department.objects.get(id=department_id) 
             sections = Section.objects.filter(department=department)
         except Department.DoesNotExist:
              return Response({'detail': f'Department with ID {department_id} not found'}, status=status.HTTP_404_NOT_FOUND)
     else:
        sections = Section.objects.all()
     serializer = SectionSerializer(sections, many=True)
     return Response(serializer.data)

   def post(self, request):
    serializer = SectionSerializer(data=request.data)
    
    if serializer.is_valid():
        department_id = request.data.get('department')
        
        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            return Response(
                {'detail': f'Department with ID {department_id} not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer.save(department=department)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class DepartmentHeadAccountManagement(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        department_heads = User.objects.filter(role="department_head")
        serializer = UserSerializer(department_heads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DepartmentHeadAccountDetail(APIView):
    permission_classes = [AllowAny]

    def put(self, request, id):
        try:
            user = User.objects.get(id=id, role='department_head')
            serializer = UserSerializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({'detail': f'User with ID {id} not found'}, status=status.HTTP_404_NOT_FOUND)

class ProgramOfficeView(APIView):
    
    def get(self, request):
        program_offices = User.objects.filter(role='program_office')
        serializer = UserSerializer(program_offices, many=True)
        return Response(serializer.data)

    def post(self, request):
       serializer = UserSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProgramOfficeDetailView(APIView):
 
  def put(self, request, id):
        try:
            program_office = User.objects.get(id=id, role='program_office')
            serializer = UserSerializer(program_office, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': f'User with ID {id} not found'}, status=status.HTTP_404_NOT_FOUND)

  def patch(self, request, id):
       try:
            program_office = User.objects.get(id=id, role='program_office')
            is_active  = request.data.get('is_active')
            program_office.is_active = is_active
            program_office.save()
            serializer = UserSerializer(program_office)
            return Response(serializer.data, status=status.HTTP_200_OK)
       except User.DoesNotExist:
               return Response({'detail': f'User with ID {id} not found'}, status=status.HTTP_404_NOT_FOUND)
class AcademicCalendarListView(APIView):

   def get(self, request):
        events = AcademicCalendar.objects.all()
        serializer = AcademicCalendarSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
   def post(self, request):
      serializer = AcademicCalendarSerializer(data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class AcademicCalendarDetailView(APIView):
     def put(self, request, id):
           try:
              event = AcademicCalendar.objects.get(id=id)
              serializer = AcademicCalendarSerializer(event, data=request.data, partial = True)
              if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status=status.HTTP_200_OK)
              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           except AcademicCalendar.DoesNotExist:
              return Response({'detail': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

     def delete(self, request, id):
         try:
             event = AcademicCalendar.objects.get(id=id)
             event.delete()
             return Response(status=status.HTTP_204_NO_CONTENT)
         except AcademicCalendar.DoesNotExist:
            return Response({'detail': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
class PasswordResetRequestView(APIView):
       def post(self, request):
           serializer = PasswordResetRequestSerializer(data=request.data)
           if serializer.is_valid():
              email = serializer.validated_data['email']
              try:
                user = User.objects.get(email=email)
              except User.DoesNotExist:
                 return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
              token = default_token_generator.make_token(user)
              uid = urlsafe_base64_encode(force_bytes(user.pk))
              reset_url = f'{settings.FRONTEND_URL}/reset-password/{uid}/{token}'  # Replace this with your frontend url
              send_mail(
                 'Password Reset Request',
                 f'Please click the following link to reset your password: {reset_url}',
                 settings.EMAIL_HOST_USER,
                 [email],
                  fail_silently=False,
              )
              return Response({'message': 'Password reset link sent to your email'}, status=status.HTTP_200_OK)
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class PasswordResetConfirmView(APIView):
        def post(self, request):
           serializer = PasswordResetConfirmSerializer(data=request.data)
           if serializer.is_valid():
              token = serializer.validated_data['token']
              new_password = serializer.validated_data['new_password']
              try:
                  uid = request.data.get('uid') #Get uid from the body
                  user_id = urlsafe_base64_decode(uid).decode()
                  user = User.objects.get(pk=user_id)
                  if default_token_generator.check_token(user, token):
                        user.password = make_password(new_password)
                        user.save()
                        return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
                  return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
              except User.DoesNotExist:
                   return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
              except:
                   return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Course, Department
from .serializers import CourseSerializer
from rest_framework.permissions import AllowAny
class CreateCourseView(APIView):
    permission_classes = [AllowAny]  #Allow any users
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
           department_id = request.data.get('department')
           try:
             department = Department.objects.get(id=department_id)
           except Department.DoesNotExist:
                return Response({'detail': f'Department with ID {department_id} not found'}, status=status.HTTP_404_NOT_FOUND)
           course = serializer.save(department=department)
           return Response(CourseSerializer(course).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDetailView(APIView):
    
    def put(self, request, id):
         try:
            course = Course.objects.get(id=id)
            serializer = CourseSerializer(course, data=request.data, partial=True)
            if serializer.is_valid():
                department_id = request.data.get('department')
                try:
                   department = Department.objects.get(id=department_id)
                except Department.DoesNotExist:
                   return Response({'detail': f'Department with ID {department_id} not found'}, status=status.HTTP_404_NOT_FOUND)
                serializer.save(department=department)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         except Course.DoesNotExist:
            return Response({'detail': f'Course with ID {id} not found'}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, id):
       try:
           course = Course.objects.get(id=id)
           course.delete()
           return Response(status=status.HTTP_204_NO_CONTENT)
       except Course.DoesNotExist:
            return Response({'detail': f'Course with ID {id} not found'}, status=status.HTTP_404_NOT_FOUND)
    def patch(self, request, id):
        try:
            course = Course.objects.get(id=id)
            serializer = CourseSerializer(course, data=request.data, partial=True)
            if serializer.is_valid():
                 serializer.save()
                 return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
               return Response({'detail': f'Course with ID {id} not found'}, status=status.HTTP_404_NOT_FOUND)
class UserListView(APIView):
     def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many =True)
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.permissions import AllowAny


class TeacherListView(APIView):
    permission_classes = [AllowAny] #Remove this later
    def get(self, request):
        teachers = User.objects.filter(role='teacher')
        serializer = UserSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
      serializer = UserSerializer(data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeacherDetailView(APIView):
    permission_classes = [AllowAny] #Remove this later
    def get(self, request, id):
        try:
            teacher = User.objects.get(id=id, role='teacher')
            serializer = UserSerializer(teacher)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': f'Teacher with ID {id} not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
       try:
            teacher = User.objects.get(id=id, role='teacher')
            serializer = UserSerializer(teacher, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       except User.DoesNotExist:
           return Response({'detail': f'Teacher with ID {id} not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            teacher = User.objects.get(id=id, role='teacher')
            teacher.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
             return Response({'detail': f'Teacher with ID {id} not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
      try:
           teacher = User.objects.get(id=id, role='teacher')
           is_active  = request.data.get('is_active')
           teacher.is_active = is_active
           teacher.save()
           serializer = UserSerializer(teacher)
           return Response(serializer.data, status=status.HTTP_200_OK)
      except User.DoesNotExist:
             return Response({'detail': f'Teacher with ID {id} not found'}, status=status.HTTP_404_NOT_FOUND)
from .serializers import DocumentSerializer
from rest_framework.parsers import MultiPartParser, FormParser 
class DocumentListView(APIView):
   parser_classes = [MultiPartParser, FormParser] 
   def get(self, request):
       documents = Document.objects.all()
       serializer = DocumentSerializer(documents, many = True)
       return Response(serializer.data, status=status.HTTP_200_OK)

   def post(self, request):
       serializer = DocumentSerializer(data=request.data)
       if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentDetailView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def get(self, request, id):
        try:
          document = Document.objects.get(id=id)
          serializer = DocumentSerializer(document)
          return Response(serializer.data, status=status.HTTP_200_OK)
        except Document.DoesNotExist:
             return Response({'detail': f'Document with ID {id} not found'}, status=status.HTTP_404_NOT_FOUND)
    def put(self, request, id):
      try:
           document = Document.objects.get(id=id)
           serializer = DocumentSerializer(document, data=request.data, partial=True)
           if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status=status.HTTP_200_OK)
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      except Document.DoesNotExist:
            return Response({'detail': f'Document with ID {id} not found'}, status=status.HTTP_404_NOT_FOUND)
    def delete(self, request, id):
         try:
            document = Document.objects.get(id=id)
            document.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
         except Document.DoesNotExist:
           return Response({'detail': f'Document with ID {id} not found'}, status=status.HTTP_404_NOT_FOUND)
###########################################################################################################################
