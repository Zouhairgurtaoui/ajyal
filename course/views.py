from typing import Any
from django.forms import ValidationError
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView,UpdateView,DeleteView,DetailView,CreateView
from django.utils.decorators import method_decorator
from users.decorators import student_required,teacher_required
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Course
from .forms import CourseCreateForm


class CourseListView(LoginRequiredMixin,ListView):
    model = Course
    ordering = ('-posted', )
    template_name = 'course/course_list.html'
    context_object_name = 'courses'
    paginate_by = 10

    def  get_queryset(self):
        if self.request.user.is_teacher:
            queryset= self.request.user.courses.annotate(course_count=Count('id', distinct=True)).order_by('-posted')
        else:
            prefetch_queryset = self.request.user.student.modules.prefetch_related('courses')
            queryset = Course.objects.filter(module__in=prefetch_queryset).distinct() .order_by('-posted') 

        return queryset

@method_decorator([login_required,teacher_required],name='dispatch')
class TeacherCourseCreateView(CreateView):
    model = Course
    form_class = CourseCreateForm
    template_name = 'course/course_add_form.html'
    

    def form_valid(self, form):
        course = form.save(commit=False)
        course.prof = self.request.user
        course.save()
        messages.success(self.request, 'The course was created with success!.')
        return redirect('course_change', course.pk)


class CourseDetailView(LoginRequiredMixin,DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'course/course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pdf_url'] = self.object.file.url
        return context

@method_decorator([login_required,teacher_required],name='dispatch')
class CourseDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Course
    template_name = 'course/course_delete_confirm.html'  
    context_object_name = 'course'
    success_url = '/course/'

    def test_func(self) -> bool | None:
        course=self.get_object()
        if course.prof == self.request.user:
            return True
        return False
@method_decorator([login_required,teacher_required],name='dispatch')
class CourseUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Course
    form_class = CourseCreateForm
    context_object_name = "course"
    template_name = 'course/course_change_form.html'
    success_url = '/course/'

    def test_func(self) -> bool | None:
        course = self.get_object()
        if course.prof == self.request.user:
            return True
        return False