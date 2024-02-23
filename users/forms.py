from django import forms
from django.contrib.auth.forms import AuthenticationForm,UsernameField
from .models import Student,Prof

class UserLoginForm(AuthenticationForm):
    username = UsernameField(label='Email or Username',
                                widget=forms.TextInput(
                                    attrs = {
                                       'placeholder': 'email or username',
                                       'class': 'form-control'
                                       }
                               ))

    password = forms.CharField(label='Password', 
                                widget=forms.PasswordInput(
                                    attrs = {
                                        'placeholder': 'password',
                                        'class': 'form-control'
                                    }
                                ))

class StudentUpdateProfile(forms.ModelForm):
    picture = forms.FileField(label='Picture',
        widget=forms.FileInput(
        attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = Student
        fields = ['picture']

class ProfUpdateProfile(forms.ModelForm):
    picture = forms.FileField(label='Picture',
                              widget=forms.FileInput(
                                  attrs = {
                                        'class': 'form-control',
                                    }
                                ))

    class Meta:
        model = Prof
        fields = ['picture']