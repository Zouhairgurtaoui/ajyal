from typing import Any
from django.forms import ValidationError
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView,UpdateView,DeleteView,DetailView,CreateView
from django.utils.decorators import method_decorator
from users.decorators import student_required,teacher_required
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Course

class CourseListView(LoginRequiredMixin,ListView):
    model = Course
    ordering = ('-posted', )
    template_name = 'course/course_list.html'
    context_object_name = 'courses'

    def  get_queryset(self):
        if self.request.user.is_teacher:
            queryset= self.request.user.courses.annotate(course_count=Count('id', distinct=True))
        else:
            prefetch_queryset = self.request.user.student.modules.prefetch_related('courses')
            queryset = Course.objects.filter(module__in=prefetch_queryset).distinct()  

        return queryset

@method_decorator([login_required,teacher_required],name='dispatch')
class TeacherCourseCreateView(CreateView):
    model = Course
    fields = ('title','file','module')
    template_name = 'course/course_add_form.html'

    def form_valid(self, form):
        file = form.cleaned_data['file']
        if not file.name.endswith('.pdf'):
            raise ValidationError('Uploaded file is not a PDF')
        course = form.save(commit=False)
        course.prof = self.request.user
        course.save()
        messages.success(self.request, 'The course was created with success!.')
        return redirect('course_change', course.pk)


class CourseDetailView(LoginRequiredMixin,DetailView):
    model = Course
    context_object_name = 'courses'
    template_name = 'course/course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pdf_url'] = self.object.file.url
        return context

       
