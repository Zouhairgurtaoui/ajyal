from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teacher:quiz_change_list')
        elif request.user.is_student:
            return redirect('student:quiz_list')
        else:
            return redirect('admin/')
    return render(request,'home.html')