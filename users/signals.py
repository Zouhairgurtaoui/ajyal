from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Prof,Student,User

'''
@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created and instance.is_student:
        Student.objects.create(user=instance)

'''
'''
@receiver(post_save,sender=Student)
def save_profile(sender,instance,**kwargs):
    if instance.is_student:
        instance.student.save()
'''

@receiver(post_save,sender=User)
def create_prof(sender,instance,created,**kwargs):
    if instance.is_teacher:
        if not hasattr(instance, 'prof'):
            Prof.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_prof(sender,instance,**kwargs):
    if instance.is_teacher:
        if hasattr(instance, 'prof'):
            instance.prof.save()

