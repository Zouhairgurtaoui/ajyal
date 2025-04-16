from django import forms
from .models import Course,Module


class CourseCreateForm(forms.ModelForm):
    title = forms.CharField(label='Course Name',
                            widget=forms.TextInput(
                                attrs={'class': 'form-control'}
                            ))
    file = forms.FileField(
        label='PDF File',
        widget=forms.FileInput(
            attrs={'class':'form-control','type':'file'}
        )
    )
    module = forms.ModelChoiceField(
        queryset=Module.objects.all(),
        label='Module',
        widget=forms.Select(
            attrs={'class':'form-control'}
        )
    )
    class Meta:
        model = Course
        fields = ('title','file','module')

    

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.endswith('.pdf'):
                return self.add_error('file',forms.ValidationError("Uploaded file is not a PDF"))
        return file
