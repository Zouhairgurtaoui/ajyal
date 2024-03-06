from django import forms
from django.contrib.auth.forms import AuthenticationForm,UsernameField,SetPasswordForm
from .models import Student,Prof, User

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
    

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='First Name',widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name',widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username','first_name','last_name']

class StudentUpdateForm(forms.ModelForm):
    picture = forms.ImageField(label='Picture',
        widget=forms.FileInput(
        attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Student
        fields = ['picture']

   

class ProfUpdateForm(forms.ModelForm):
    picture = forms.ImageField(label='Picture',
                              widget=forms.FileInput(
                                  attrs = {
                                        'class': 'form-control',
                                    }
                                ))

    class Meta:
        model = Prof
        fields = ['picture']


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password',
                                    widget=forms.PasswordInput(
                                        attrs={'class':'form-control'}
                                    ))
    new_password2 = forms.CharField(label='Confirm New Password',
                                    widget=forms.PasswordInput(
                                        attrs={'class':'form-control'}
                                    ))
    