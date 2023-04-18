from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import connection

class CustomUser(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    ROLES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLES)

class Course(models.Model):
    SUBJECTS = (
        ('math', 'Math'),
        ('grammar', 'Grammar'),
        ('history', 'History'),
        ('physics', 'Physics'),
    )

    GRADES = (
        (4, 'Grade 4'),
        (5, 'Grade 5'),
        (6, 'Grade 6'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=20, choices=SUBJECTS)
    grade_level = models.IntegerField(choices=GRADES)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.title

def reset_courses():
    # Delete all courses
    Course.objects.all().delete()

    # Reset primary key sequence for the Course model
    with connection.cursor() as cursor:
        cursor.execute(f"ALTER SEQUENCE {Course._meta.db_table}_id_seq RESTART WITH 1;")
