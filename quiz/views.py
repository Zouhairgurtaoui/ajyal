from django.forms import inlineformset_factory
from django.shortcuts import redirect, render,get_object_or_404
from django.views.generic import (ListView,CreateView,UpdateView,DeleteView,DetailView)
from django.utils.decorators import method_decorator
from course.models import Course
from users.decorators import student_required,teacher_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.db import transaction
from django.db.models import Count,Avg
from django.urls import reverse, reverse_lazy

from .models import Answer, Question, Quiz
from .forms import BaseAnswerInlineFormSet, QuestionForm, TakeQuizForm
from users.models import TakenQuiz


@method_decorator([login_required, teacher_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('-date_created', )
    context_object_name = 'quizzes'
    template_name = 'quiz/prof/quiz_change_list.html'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = self.request.user.quizzes \
            .select_related('course') \
            .annotate(questions_count=Count('questions', distinct=True)) \
            .annotate(taken_count=Count('taken_quizzes', distinct=True)).order_by('-date_created')
        return queryset


@method_decorator([login_required, teacher_required], name='dispatch')
class QuizCreateView(CreateView):
    model = Quiz
    fields = ('name', 'course', )
    template_name = 'quiz/prof/quiz_add_form.html'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.owner = self.request.user
        quiz.save()
        messages.success(self.request, 'The quiz was created with success! Go ahead and add some questions now.')
        return redirect('teacher:quiz_change', quiz.pk)

@method_decorator([login_required, teacher_required], name='dispatch')
class QuizUpdateView(UserPassesTestMixin,UpdateView):
    model = Quiz
    fields = ('name', 'course', )
    context_object_name = 'quiz'
    template_name = 'quiz/prof/quiz_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.quizzes.all()
    
    def test_func(self) -> bool | None:
        quiz = self.get_object()
        if self.request.user == quiz.owner:
            return True
        return False

    def get_success_url(self):
        return reverse('teacher:quiz_change', kwargs={'pk': self.object.pk})

@method_decorator([login_required, teacher_required], name='dispatch')
class QuizDeleteView(UserPassesTestMixin,DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'quiz/prof/quiz_delete_confirm.html'
    success_url = reverse_lazy('teacher:quiz_change_list')

    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, 'The quiz %s was deleted with success!' % quiz.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()
    
    def test_func(self) -> bool | None:
        quiz = self.get_object()
        if self.request.user == quiz.owner:
            return True
        return False


@method_decorator([login_required, teacher_required], name='dispatch')
class QuizResultsView(UserPassesTestMixin,DetailView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'quiz/prof/quiz_results.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        quiz = self.get_object()
        taken_quizzes = quiz.taken_quizzes.select_related('student__user').order_by('-date')
        total_taken_quizzes = taken_quizzes.count()
        quiz_score = quiz.taken_quizzes.aggregate(average_score=Avg('score'))
        extra_context = {
            'taken_quizzes': taken_quizzes,
            'total_taken_quizzes': total_taken_quizzes,
            'quiz_score': quiz_score
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all().order_by('-date_created')
    
    def test_func(self) -> bool | None:
        quiz = self.get_object()
        if self.request.user == quiz.owner:
            return True
        return False

@login_required
@teacher_required
def question_add(request, pk):
    # By filtering the quiz by the url keyword argument `pk` and
    # by the owner, which is the logged in user, we are protecting
    # this view at the object-level. Meaning only the owner of
    # quiz will be able to add questions to it.
    quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, 'You may now add answers/options to the question.')
            return redirect('teacher:question_change', quiz.pk, question.pk)
    else:
        form = QuestionForm()

    return render(request, 'quiz/prof/question_add_form.html', {'quiz': quiz, 'form': form})


@login_required
@teacher_required
def question_change(request, quiz_pk, question_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk, owner=request.user)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

    AnswerFormSet = inlineformset_factory(
        Question,  
        Answer,
        formset=BaseAnswerInlineFormSet,
        fields=('text', 'is_correct'),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, 'Question and answers saved with success!')
            return redirect('teacher:quiz_change', quiz.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)

    return render(request, 'quiz/prof/question_change_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'formset': formset
    })


@method_decorator([login_required, teacher_required], name='dispatch')
class QuestionDeleteView(UserPassesTestMixin,DeleteView):
    model = Question
    context_object_name = 'question'
    template_name = 'quiz/prof/question_delete_confirm.html'
    pk_url_kwarg = 'question_pk'

    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs['quiz'] = question.quiz
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        question = self.get_object()
        messages.success(request, 'The question %s was deleted with success!' % question.text)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Question.objects.filter(quiz__owner=self.request.user)
    
    def test_func(self) -> bool | None:
        question = self.get_object()
        if self.request.user == question.quiz.owner:
            return True
        return False

    def get_success_url(self):
        question = self.get_object()
        return reverse('teacher:quiz_change', kwargs={'pk': question.quiz_id})


@method_decorator([login_required, student_required], name='dispatch')
class StudentQuizListView(ListView):
    model = Quiz
    ordering = ('-date_created', )
    context_object_name = 'quizzes'
    template_name = 'quiz/student/quiz_list.html'
    paginate_by = 10
    def get_queryset(self):
        student = self.request.user.student
        student_modules = student.modules.all()
        student_courses = Course.objects.filter(module__in=student_modules)
        taken_quizzes = student.quizzes.values_list('pk', flat=True)
        queryset = Quiz.objects.filter(course__in=student_courses) \
            .exclude(pk__in=taken_quizzes) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset
    
@method_decorator([login_required, student_required], name='dispatch')
class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'quiz/student/taken_quiz_list.html'
    paginate_by = 10
    def get_queryset(self):
        queryset = self.request.user.student.taken_quizzes \
            .select_related('quiz', 'quiz__course') \
            .order_by('quiz__date_created')
        return queryset

@login_required
@student_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.student

    if student.quizzes.filter(pk=pk).exists():
        return render(request, 'quiz/student/taken_quiz_list.html')

    total_questions = quiz.questions.count()
    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    try:
        progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    except ZeroDivisionError:
        messages.error(request,"This Quiz Has no Question yet")
        return redirect('student:quiz_list')
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                is_quiz_end = request.POST.get('is_quiz_end')
                if is_quiz_end == 'true':
                    correct_answers = student.quiz_student_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2) 
                    TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
                    if score < int(total_questions/2):
                        messages.warning(request, 'Better luck next time! Your score for the %s was %s.' % (quiz.name, score))
                    else:
                        messages.success(request, 'Congratulations! You completed the %s with success! You scored %s points.' % (quiz.name, score))
                    return redirect('student:quiz_list')
                elif student.get_unanswered_questions(quiz).exists():
                    return redirect('student:take_quiz', pk)
                else:
                    correct_answers = student.quiz_student_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
                    if score < int(total_questions/2):
                        messages.warning(request, 'Better luck next time! Your score for the %s was %s.' % (quiz.name, score))
                    else:
                        messages.success(request, 'Congratulations! You completed the %s with success! You scored %s points.' % (quiz.name, score))
                    return redirect('student:quiz_list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'quiz/student/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress
    })

@login_required
def search_quiz(request):
    search_text = request.POST.get('search')
    if search_text == '':
        return render(request,'quiz/_search_results.html')
    if request.user.is_student:
        results = Quiz.objects.filter(name__icontains = search_text,course__in=request.user.courses)
    else:
        results = Quiz.objects.filter(name__icontains=search_text,owner=request.user)

    context = {
        'results':results
    }

    return render(request,'quiz/_search_results.html',context)