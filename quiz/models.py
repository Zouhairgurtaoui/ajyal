from django.db import models
from django.utils import timezone
from course.models import Course



class Quiz(models.Model):
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    date_created = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return self.name
    
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(null=False)
    date_created = models.DateTimeField(auto_now_add=timezone.now)
    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)
    date_created = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self) -> str:
        return self.text


class StudentAnswer(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='quiz_student_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')