from django import forms

from courses.models import Course
from homework.models import HomeworkAssignment, ReadingAssignment


class HomeworkAssignmentForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(user=1),
        widget=forms.Select(attrs={'class': 'form-control form-control-lg'})
    )

    class Meta:
        model = HomeworkAssignment
        exclude = ['completed']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': '4'}),
            'course': forms.Select(attrs={'class': 'form-control form-control-lg'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control form-control-lg', 'type': 'date'}),
            'due_time': forms.TimeInput(attrs={'class': 'form-control form-control-lg', 'type': 'time'}),
            'link': forms.URLInput(attrs={'class': 'form-control form-control-lg'}),
        }

    def __init__(self, *args, **kwargs):
        # Defines the user from the kwargs to prevent the multiple values error
        user = kwargs.pop('user', None)
        super(HomeworkAssignmentForm, self).__init__(*args, **kwargs)
        # Changes the user from the default to the request
        self.fields['course'].queryset = Course.objects.filter(user=user)


class ReadingAssignmentForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(user=1),
        widget=forms.Select(attrs={'class': 'form-control form-control-lg'})
    )

    class Meta:
        model = ReadingAssignment
        exclude = ['completed', 'uploaded']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': '4'}),
            'course': forms.Select(attrs={'class': 'form-control form-control-lg'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control form-control-lg', 'type': 'date'}),
            'due_time': forms.TimeInput(attrs={'class': 'form-control form-control-lg', 'type': 'time'}),
            'link': forms.URLInput(attrs={'class': 'form-control form-control-lg'}),
            'start_page': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'end_page': forms.TextInput(attrs={'class': 'form-control form-control-lg'})
        }

    def __init__(self, *args, **kwargs):
        # Defines the user from the kwargs to prevent the multiple values error
        user = kwargs.pop('user', None)
        super(ReadingAssignmentForm, self).__init__(*args, **kwargs)
        # Changes the user from the default to the request
        self.fields['course'].queryset = Course.objects.filter(user=user)
