from django.contrib import admin
from .models import Notification,QuizNotification,CourseNotification


admin.site.register(Notification)

admin.site.register(QuizNotification)

admin.site.register(CourseNotification)
