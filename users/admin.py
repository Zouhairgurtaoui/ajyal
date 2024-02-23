from django.contrib import admin
from .models import User,Prof,Student
from django.core import validators
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm


class CNEValidation(validators.RegexValidator):
   regex=r"^[A-Za-z]\d{9}$"
   message = _("Enter a valid CNE number.It should start with a letter followed by 9 digits")
   flags = 0

class StudentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['cne'].validators.append(CNEValidation())


class StudentAdmin(admin.ModelAdmin):
   form = StudentForm
   fields = ('cne','picture','user','date_naissance','filliere','modules')
 
 


admin.site.register(User)

admin.site.register(Student,StudentAdmin)

admin.site.register(Prof)