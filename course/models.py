

from django.db import models

from django.utils import timezone
# Create your models here.

def user_directory_path(instance, filename):
	
	return f'{instance.prof.username}_courses/{filename}'


class Filliere(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name

class Module(models.Model):
    name = models.CharField(max_length=100)
    filliere = models.ManyToManyField(Filliere, related_name='modules')

    def __str__(self) -> str:
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(default='default_course_img.jpeg')
    file = models.FileField(upload_to=user_directory_path)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='courses')
    prof = models.ForeignKey('users.User',on_delete=models.CASCADE,related_name='courses')
    posted = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self) -> str:
         return self.title
    class Meta:
        ordering = ('-posted',)