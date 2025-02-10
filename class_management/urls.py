from django.urls import path
from .views import (
    RegisterUserView,
    ClassScheduleView,
    AttendanceView,
    QABulletinView,
    FastPacedGameView,
    TodoListView,
    TaskDetailView,
    AcademicCalendarView,
    NotificationsView,
    AccountManagementView,
    LoginView,
    ChangePasswordView,
    CreateRegistrarView,
    UpdateRegistrarStatus,
    SemesterScheduleListView, 
    SemesterScheduleDetailView,
    DepartmentDetailView,
    DepartmentListView,
    RoleListView,
    TeacherListView,
    AttendanceListView,
    StudentAttendanceView,
    CreateCourseView,
    SectionListView,
    DepartmentHeadAccountManagement,
    DepartmentHeadAccountDetail,
    ProgramOfficeDetailView,
    ProgramOfficeView,
    AcademicCalendarListView,
    CourseDetailView,
    TeacherDetailView,
    DocumentListView,
    DocumentDetailView
)
urlpatterns = [
    # User Registration
    path('user/', RegisterUserView.as_view(), name='user-create'),
    path('register/', RegisterUserView.as_view(), name='register'),
 path('login/', LoginView.as_view(), name='login'),
 path('user/<uuid:id>/change-password/', ChangePasswordView.as_view(), name='change-password'),
 # Registrar Endpoints
        path('registrars/', CreateRegistrarView.as_view(), name='create-registrar'),
         path('registrars/<uuid:id>/', UpdateRegistrarStatus.as_view(), name='update-registrar-status'),
    # Student-related Views
    path('students/<uuid:id>/schedule/', ClassScheduleView.as_view(), name='class-schedule'),
    path('students/<uuid:id>/attendance/', AttendanceView.as_view(), name='attendance'),
    path('students/<uuid:id>/tasks/', TodoListView.as_view(), name='tasks-list'),
    path('students/<uuid:id>/tasks/<uuid:task_id>/', TaskDetailView.as_view(), name='task-detail'),
    path('students/<uuid:id>/notifications/', NotificationsView.as_view(), name='notifications'),
    path('students/<uuid:id>/', AccountManagementView.as_view(), name='account-management'),

    # General Views
    path('qa-bulletin/', QABulletinView.as_view(), name='qa-bulletin'),
    path('fast-paced-game/', FastPacedGameView.as_view(), name='fast-paced-game'),
    path('academic-calendar/', AcademicCalendarView.as_view(), name='academic-calendar'),
    #schedule routes
        path('schedules/', SemesterScheduleListView.as_view(), name='schedule-list'),  
        path('schedules/<uuid:id>/', SemesterScheduleDetailView.as_view(), name='schedule-detail'), 
        path('schedules/classroom/<str:classroom>/', ClassScheduleView.as_view(), name='schedule-by-classroom'),
        #department routes
         path('departments/', DepartmentListView.as_view(), name='department-list'),
         path('departments/<uuid:id>/', DepartmentDetailView.as_view(), name='department-detail'),
         #roles
     path('roles/', RoleListView.as_view(), name='role-list'),
     path('teachers/', TeacherListView.as_view(), name='teacher-list'),
        path('teachers/<uuid:id>/', TeacherDetailView.as_view(), name='teacher-detail'),

     path('attendances/', AttendanceListView.as_view(), name='attendance-list'),
     path('student-attendances/', StudentAttendanceView.as_view(), name='student-attendance-list'),
     #course
     path('courses/', CreateCourseView.as_view(), name='create-course'),
     path('sections/', SectionListView.as_view(), name='section-list'),
     path('departments/<uuid:department_id>/sections/', SectionListView.as_view(), name='section-list-by-department'),
     path('courses/<uuid:id>/', CourseDetailView.as_view(), name='update-course'),
     #department heads
       path('department-heads/', DepartmentHeadAccountManagement.as_view(), name='department-head-list'),
    path('department-heads/<uuid:id>/', DepartmentHeadAccountDetail.as_view(), name='department-head-detail'),
    path('program-offices/', ProgramOfficeView.as_view(), name='program-offices-list'),
    path('program-offices/<uuid:id>/', ProgramOfficeDetailView.as_view(), name='program-office-detail'),
    #Academic Calendar
  path('academic-calendars/', AcademicCalendarListView.as_view(), name='academic-calendar-list'),
      #Document Routes
     path('documents/', DocumentListView.as_view(), name='document-list'),
     path('documents/<uuid:id>/', DocumentDetailView.as_view(), name='document-detail'),
]
