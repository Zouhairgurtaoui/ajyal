from django import forms

from course.models import Filliere
from .models import Notification


class NotificationAddForm(forms.ModelForm):
    content = forms.CharField(label='Your Content Here',widget=forms.Textarea(attrs={'class':'form-control'}))
    filliere = forms.ModelChoiceField(label='Filliere',widget=forms.Select(attrs={'class':'form-control'}),queryset=Filliere.objects.all())

    class Meta:
        model = Notification
        fields = ('content','filliere')

