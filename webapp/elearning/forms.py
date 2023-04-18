from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Course, Lesson

class CustomUserCreationForm(UserCreationForm):
    is_teacher = forms.BooleanField(required=False, initial=False, label="Register as teacher")
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role', 'is_teacher']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'subject', 'grade_level']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'order']