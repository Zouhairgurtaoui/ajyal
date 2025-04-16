from django.db import models
from users.models import User
from course.models import Course,Filliere
from quiz.models import Quiz
from django.utils import timezone

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE,related_name='notifications')
    is_for_teacher = models.BooleanField(default=False)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=timezone.now)
    filliere  = models.ForeignKey(Filliere,on_delete=models.PROTECT)
    is_quiz_notif = models.BooleanField(default=False)
    is_course_notif = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.content

class CourseNotification(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE, related_name='course_notifications')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  

    def __str__(self) -> str:
        return self.notification.content

class QuizNotification(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE, related_name='quiz_notifications')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.notification.content

