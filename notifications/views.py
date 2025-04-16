
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import Notification
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,ListView,DeleteView,UpdateView
from users.decorators import student_required,teacher_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NotificationAddForm

@login_required
def change_stat(request,pk):
    try:
        notification = Notification.objects.get(pk=pk)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success':True})
    except Notification.DoesNotExist:
        return JsonResponse({'success':False})
    


    
@method_decorator([teacher_required,],name='dispatch')
class NotificationCreateView(LoginRequiredMixin,CreateView):
    model=Notification
    template_name = 'notification/notification_create.html'
    form_class = NotificationAddForm
    success_url = '/course/'

    def form_valid(self, form):
        notif = form.save(commit=False)
        notif.recipient = self.request.user
        notif.save()
        return super().form_valid(form)

    