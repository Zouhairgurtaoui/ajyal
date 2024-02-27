from django.db.models.signals import post_save
from django.dispatch import receiver
from course.models import Course
from quiz.models import Quiz
from users.models import  VisitedCourses, TakenQuiz
from .models import Notification,QuizNotification,CourseNotification

@receiver(post_save, sender=VisitedCourses)
def create_visited_course_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(recipient=instance.course.prof, content=f'{instance.student.user.username} visited your course "{instance.course.title}".',filliere=instance.student.filliere,is_for_teacher=True)

@receiver(post_save, sender=TakenQuiz)
def create_taken_quiz_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(recipient=instance.quiz.owner, content=f'{instance.student.user.username} took your quiz "{instance.quiz.name}".',filliere=instance.student.filliere,is_for_teacher=True)

@receiver(post_save, sender=Course)
def create_course_notification(sender, instance, created, **kwargs):
    if created :
        Notification.objects.create(
                recipient=instance.prof,
                content=f'A new course "{instance.title}" has been created.',
                filliere = instance.module.filliere.first(),
                is_course_notif=True
            )

@receiver(post_save, sender=Quiz)
def create_quiz_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
                recipient=instance.owner,
                content=f'A new quiz "{instance.name}" has been created.',
                filliere = instance.course.module.filliere.first(),
                is_quiz_notif=True
            )


@receiver(post_save, sender=Notification)
def create_type_notification(sender, instance, created, **kwargs):
    if created and instance.is_quiz_notif:
        QuizNotification.objects.create(
            notification = instance,
            quiz = Quiz.objects.filter(owner=instance.recipient).order_by('-date_created').first()
        )
    elif created and instance.is_course_notif:
        CourseNotification.objects.create(
            notification = instance,
            course = Course.objects.filter(prof=instance.recipient).order_by('-posted').first()
        )