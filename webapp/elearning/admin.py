from django.contrib import admin
from .models import CustomUser, Course, Lesson
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'grade_level')
    list_filter = ('subject', 'grade_level')
    search_fields = ('title',)

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title',)

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
