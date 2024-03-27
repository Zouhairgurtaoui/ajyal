from django import forms
from django.contrib.auth.forms import AuthenticationForm,UsernameField,SetPasswordForm
from .models import Student,Prof, User,Contact

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


class ContactForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control',
               'id':'name',
               'placeholder':'Enter your name...',
               'data-sb-validations':'required'}
               ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class':'form-control',
               'id':'email',
               'placeholder':'Enter your acadimic email...',
               'data-sb-validations':'required'
               }
    ))
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'id':'phone',
            'type':"tel",
            'placeholder':'+212 634-567-890',
            'data-sb-validations':'required'
        }
    ))
    message = forms.CharField(widget=forms.Textarea(
         attrs={'class':'form-control',
               'id':'message',
               'placeholder':'Enter your message here...',
               'data-sb-validations':'required',
                'style':"height: 10rem"
               }
    ))

    class Meta:
        model = Contact
        fields = ('__all__')
