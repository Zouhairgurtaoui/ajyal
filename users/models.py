from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils.translation import gettext_lazy as _
from course.models import Filliere,Module,Course
from quiz.models import Answer, Quiz
from PIL import Image
from django.conf import settings
import os
from django.utils import timezone



def user_directory_path_profile(instance, filename):
    
	profile_pic_name = f'{instance.user.username}_{instance.user.id}/profile.jpg'
	full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

	if os.path.exists(full_path):
		os.remove(full_path)
	
	return profile_pic_name

class User(AbstractUser):
	is_student = models.BooleanField(default=False)
	is_teacher = models.BooleanField(default=False)
	email = models.EmailField(unique=True)

	
	
	

class Student(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
	cne = models.CharField(max_length=10,unique=True)
	modules = models.ManyToManyField(Module, related_name='students')
	filliere = models.ForeignKey(Filliere, on_delete=models.CASCADE, related_name='students')
	quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
	courses = models.ManyToManyField(Course,through='VisitedCourses')
	date_naissance=models.DateField(null=True,blank=True)
	picture = models.ImageField(upload_to=user_directory_path_profile,default='default.jpg')

	def get_unanswered_questions(self, quiz):
		answered_questions = self.quiz_student_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
		questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
		return questions

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		SIZE = 516, 516

		if self.picture:
			pic = Image.open(self.picture.path)
			pic.thumbnail(SIZE, Image.LANCZOS)
			pic.save(self.picture.path)

	
	def __str__(self):
		return self.cne
		
	
class Prof(models.Model):
	picture = models.ImageField(upload_to=user_directory_path_profile,null=True,default='default.jpg')
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	date_naissance=models.DateField(null=True,blank=True)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		SIZE = 416, 416

		if self.picture:
			pic = Image.open(self.picture.path)
			pic.thumbnail(SIZE, Image.LANCZOS)
			pic.save(self.picture.path)


	def __str__(self) -> str:
		return self.user.username

class TakenQuiz(models.Model):
	date = models.DateField(auto_now_add=timezone.now)
	student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quizzes')
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
	score = models.IntegerField()
	
class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')

class VisitedCourses(models.Model):
	student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='visited_courses')
	course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='visited_courses')
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	duration = models.DurationField()
	formatted_duration = models.CharField(max_length=100,null=True)



class Contact(models.Model):
	full_name = models.CharField(max_length=255)
	email  = models.EmailField(max_length=255)
	phone_number = models.CharField(max_length=14)
	message = models.TextField()

	def __str__(self):
		return self.full_name
	
