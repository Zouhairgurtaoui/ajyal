from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView,UpdateView,DeleteView,DetailView
from django.utils.decorators import method_decorator
from users.decorators import student_required,prof_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course

