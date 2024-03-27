from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Prof,Student,Contact
from django.core import validators
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


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
 
 
class CustomUserAdmin(UserAdmin):
   form = MyUserChangeForm
   fieldsets = UserAdmin.fieldsets + (
            (_('User Type'), {
               'fields': ('is_student','is_teacher')
               }),
    )



admin.site.register(User,CustomUserAdmin)

admin.site.register(Student,StudentAdmin)

admin.site.register(Prof)
admin.site.register(Contact)