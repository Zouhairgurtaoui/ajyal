from django.shortcuts import render
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from users.decorators import student_required,prof_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models import Count

from .models import Quiz


@method_decorator([login_required, student_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('-date_created', )
    context_object_name = 'quizzes'
    template_name = 'quiz/quiz_list.html'

    def get_queryset(self):
        student = self.request.user.student
        student_courses = student.modules.courses.values_list('pk', flat=True)
        taken_quizzes = student.quizzes.values_list('pk', flat=True)
        queryset = Quiz.objects.filter(course__in=student_courses) \
            .exclude(pk__in=taken_quizzes) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset