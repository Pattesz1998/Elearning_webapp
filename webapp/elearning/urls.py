from django.urls import path
from . import views

app_name = 'elearning'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('teacher_dashboard/', views.TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('student_dashboard/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('course_create/', views.CourseCreateView.as_view(), name='course_create'),
    path('course_update/<int:pk>/', views.CourseUpdateView.as_view(), name='course_update'),
    path('course_delete/<int:pk>/', views.CourseDeleteView.as_view(), name='course_delete'),
    path('lesson_update/<int:pk>/', views.LessonUpdateView.as_view(), name='lesson_update'),
    path('lesson_delete/<int:pk>/', views.LessonDeleteView.as_view(), name='lesson_delete'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('course/<int:pk>/lesson_create/', views.LessonCreateView.as_view(), name='lesson_create'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
path('lesson_content/<int:pk>/', views.lesson_content, name='lesson_content'),
]