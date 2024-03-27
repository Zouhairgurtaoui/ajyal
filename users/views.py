import datetime



from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Student, User,VisitedCourses
from course.models import Module,Course
from django.contrib import messages
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .decorators import teacher_required
from django.db.models import Count,Max
from .forms import UserUpdateForm,ProfUpdateForm,StudentUpdateForm,ContactForm

def index(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            if not request.user.last_login:
               return redirect('user_profile',request.user.username) 
            return redirect('course_list')
        elif request.user.is_teacher:
            if not request.user.last_login:
               return redirect('user_profile',request.user.username) 
            return redirect('student_list')
        else:
            return redirect('admin/')
    return redirect('user-login')

@login_required
def profile(request,username):
    user = get_object_or_404(User,username=username)
    if user.is_student:
        taken_quizzes = user.student.taken_quizzes.select_related('quiz', 'quiz__course').filter(quiz__course__prof=request.user).order_by('-quiz__date_created')
        visited_courses = user.student.visited_courses.filter(course__prof=request.user).select_related('course', 'course__module').order_by('-duration')
        context = {
                'user_p':user,
                'taken_quizzes':taken_quizzes,
                'visited_courses':visited_courses,
                }
        return render(request,'user/student_profile.html',context=context)
    else:
        courses= user.courses.all()
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
        queryset = Student.objects.filter(modules__in=modules).annotate(
            max_quiz_score=Max('taken_quizzes__score'),
            duration=Max('visited_courses__duration')
        ).order_by('max_quiz_score','duration')
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
                return redirect('edit_profile')
        else:
            u_form = UserUpdateForm(request.POST,instance=request.user)
            p_form = StudentUpdateForm(request.POST,request.FILES,instance=request.user.student)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request,'your account has been Updated!')
                return redirect('edit_profile')
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

@login_required
def store_reading_time(request,pk):
    if request.method == 'POST':
        course = get_object_or_404(Course,pk=pk)
        exist = VisitedCourses.objects.filter(course = course).exists()

        visited_course = VisitedCourses.objects.get(course = course) if exist else None
        
        
        start_time = datetime.datetime.fromisoformat(request.POST['start_time'])
        end_time = datetime.datetime.fromisoformat(request.POST['end_time'])
            
        duration_microseconds = end_time - start_time
        days, seconds = duration_microseconds.days, duration_microseconds.seconds
        hours = int(days * 24 + seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        seconds = int(seconds % 60)
        
        formatted_duration = f'{hours} h: {minutes} min: {seconds} sec'

        if not exist:
            visited_course = VisitedCourses.objects.create(
                student=request.user.student,
                course=course,
                start_time=start_time,
                end_time=end_time,
                duration=duration_microseconds,
                formatted_duration=formatted_duration
            )
            return JsonResponse({'success': True})
        
        visited_course.duration = duration_microseconds
        visited_course.formatted_duration = formatted_duration
        visited_course.save()
    return JsonResponse({'success': True})

@login_required
def search_student(request):
    search_text = request.POST.get('search')

    results = Student.objects.filter(user__username__icontains = search_text,courses__prof=request.user).distinct()

    context = {
        'results':results
    }

    return render(request,'user/_search_results.html',context)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Message was sent succesfully. We will respond as soon as we can")
            return redirect('user-login')
    else:
        form = ContactForm()

    return render(request,'contact.html',context={
        'form':form
    })        