from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from .models import Notification
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,ListView,DeleteView,UpdateView
from users.decorators import student_required,teacher_required
from django.contrib.auth.mixins import UserPassesTestMixin

@login_required
def change_stat(request,pk):
    try:
        notification = Notification.objects.get(pk=pk)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success':True})
    except Notification.DoesNotExist:
        return JsonResponse({'success':False})

