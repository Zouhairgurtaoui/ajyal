from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Student, User
from course.models import Module
from django.contrib import messages
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .decorators import teacher_required
from django.db.models import Count
from .forms import UserUpdateForm,ProfUpdateForm,StudentUpdateForm

def index(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teacher:quiz_change_list')
        elif request.user.is_student:
            return redirect('student:quiz_list')
        else:
            return redirect('admin/')
    return render(request,'home.html')

@login_required
def profile(request,username):
    user = get_object_or_404(User,username=username)
    if user.is_student:
        taken_quizzes = user.student.taken_quizzes.select_related('quiz', 'quiz__course').filter(quiz__course__prof=request.user).order_by('-quiz__date_created')
        visited_courses = user.student.visited_courses.select_related('course', 'course__module').order_by('-duration')
        context = {
                'user_p':user,
                'taken_quizzes':taken_quizzes,
                'visited_courses':visited_courses,
                }
        return render(request,'user/student_profile.html',context=context)
    else:
        courses= user.courses
        quizzes = user.quizzes.annotate(questions_count=Count('questions', distinct=True))

        context = {
            'user_p':user,
            'courses':courses,
            'quizzes':quizzes
        }
        return render(request,'user/teacher_profile.html',context=context)

@method_decorator([login_required,teacher_required],name='dispatch')
class StudentListView(ListView):
    model = Student
    context_object_name = 'students'
    template_name = 'user/student_list.html'

    def get_queryset(self):
        teacher_courses = self.request.user.courses.all()
        modules = Module.objects.filter(courses__in=teacher_courses)
        queryset = Student.objects.filter(modules__in=modules)
        return queryset
@login_required
def edit_profile(request):
    if request.method == "POST":
        if request.user.is_teacher:
            u_form = UserUpdateForm(request.POST,instance=request.user)
            p_form = ProfUpdateForm(request.POST,request.FILES,instance=request.user.prof)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request,'your account has been Updated!')
                return redirect('teacher_profile')
            else:
                u_form = UserUpdateForm(request.POST,instance=request.user)
                p_form = StudentUpdateForm(request.POST,request.FILES,instance=request.user.student)
                if u_form.is_valid() and p_form.is_valid():
                    u_form.save()
                    p_form.save()
                    messages.success(request,'your account has been Updated!')
                    return redirect('student_profile')
    else:
        if request.user.is_teacher:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfUpdateForm(instance=request.user.prof)
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = StudentUpdateForm(instance=request.user.student)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }


    return render(request,'user/edit_profile.html',context)