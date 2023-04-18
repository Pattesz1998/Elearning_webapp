from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Course, Lesson
from .forms import CustomUserCreationForm, CourseForm, LessonForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.is_teacher:
                return redirect('elearning:teacher_dashboard')
            else:
                return redirect('elearning:student_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'elearning/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_teacher:
                return redirect('elearning:teacher_dashboard')
            else:
                return redirect('elearning:student_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'elearning/login.html')

def logout_view(request):
    logout(request)
    return redirect('elearning:login')

@login_required
def user_profile(request):
    return render(request, 'elearning/user_profile.html')

@login_required
def dashboard(request):
    if request.user.role == 'teacher':
        return redirect('elearning:teacher_dashboard')
    else:
        return redirect('elearning:student_dashboard')

@login_required
def course_detail(request, pk):
    course = Course.objects.get(pk=pk)
    lessons = Lesson.objects.filter(course=course).order_by('order')

    context = {
        'course': course,
        'lessons': lessons,
    }

    return render(request, 'elearning/course_detail.html', context)

class TeacherDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'elearning/teacher_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.filter(teacher=self.request.user)
        context['course_form'] = CourseForm()
        context['lesson_form'] = LessonForm()

        # Add lessons for each course to the context
        course_lessons = {}
        for course in context['courses']:
            lessons = Lesson.objects.filter(course=course)
            course_lessons[course.id] = lessons
        context['course_lessons'] = course_lessons

        return context

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_teacher

    def post(self, request, *args, **kwargs):
        if 'create_course' in request.POST:
            course_form = CourseForm(request.POST)
            if course_form.is_valid():
                course = course_form.save(commit=False)
                course.teacher = request.user
                course.save()
        elif 'create_lesson' in request.POST:
            lesson_form = LessonForm(request.POST)
            if lesson_form.is_valid():
                lesson = lesson_form.save(commit=False)
                lesson.course = Course.objects.get(pk=request.POST.get('course'))
                lesson.save()
        return redirect('teacher_dashboard')

class StudentDashboardView(UserPassesTestMixin, ListView):
    model = Course
    template_name = 'elearning/student_dashboard.html'
    context_object_name = 'courses'

    def test_func(self):
        return self.request.user.role == 'student'

class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'elearning/course_create.html'
    success_url = reverse_lazy('elearning:teacher_dashboard')

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)

class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'elearning/course_update.html'
    success_url = reverse_lazy('elearning:teacher_dashboard')

    def test_func(self):
        return self.request.user.is_teacher

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)


class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    template_name = 'elearning/course_delete.html'
    success_url = reverse_lazy('elearning:teacher_dashboard')

    def test_func(self):
        return self.request.user.is_teacher

class LessonCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'elearning/lesson_create.html'

    def get_success_url(self):
        return reverse_lazy('elearning:teacher_dashboard', kwargs={'pk': self.object.course.pk})

    def form_valid(self, form):
        course = Course.objects.get(pk=self.kwargs['pk'])
        form.instance.course = course
        return super().form_valid(form)

    def test_func(self):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        return self.request.user == course.teacher

class LessonUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'elearning/lesson_update.html'

    def get_success_url(self):
        return reverse_lazy('elearning:teacher_dashboard', kwargs={'pk': self.object.course.pk})

    def test_func(self):
        lesson = self.get_object()
        return self.request.user == lesson.course.teacher

class LessonDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Lesson
    template_name = 'elearning/lesson_delete.html'

    def get_success_url(self):
        return reverse_lazy('elearning:teacher_dashboard', kwargs={'pk': self.object.course.pk})

    def test_func(self):
        lesson = self.get_object()
        return self.request.user == lesson.course.teacher

def lesson_content(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    return render(request, 'elearning/lesson_content.html', {'lesson': lesson})