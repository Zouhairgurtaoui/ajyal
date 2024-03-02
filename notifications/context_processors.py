from .models import Notification
from django.db.models import Count

def notifications(request):
    if request.user.is_authenticated:
        notifications = None
        notification_count = None
        if request.user.is_student:
            notifications = Notification.objects.filter(filliere=request.user.student.filliere,is_read=False,is_for_teacher=False).order_by('-timestamp')
            notification_count = notifications.filter(is_read=False).count()
            return {'notifications': notifications[:5] if notifications else None,'notification_count':notification_count} 
        elif request.user.is_teacher:
            notifications = request.user.notifications.filter(is_read=False,is_for_teacher=True).order_by('-timestamp')
            notification_count = notifications.filter(is_read=False).count()
            return {'notifications': notifications[:5] if notifications else None,'notification_count':notification_count} 
                 
    return {}
