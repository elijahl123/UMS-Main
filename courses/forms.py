import ast

from django import forms
from django.forms import ModelForm

from courses.models import *


class CourseForm(ModelForm):
    class Meta:
        model = Course
        exclude = []

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'
            visible.field.widget.attrs['rows'] = '4'


class CourseTimeForm(ModelForm):
    weekday_choices = [
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    class Meta:
        model = CourseTime
        exclude = []


class CourseTimeEditForm(ModelForm):
    weekday_choices = [
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    weekday = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(choices=weekday_choices),
        choices=weekday_choices
    )

    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(user=1),
        widget=forms.Select(attrs={'class': 'form-control form-control-lg'})
    )

    class Meta:
        model = CourseTime
        exclude = []
        widgets = {
            'start_time': forms.TimeInput(
                attrs={'class': 'form-control form-control-lg', 'type': 'time', 'min': '08:00', 'max': '22:00'}),
            'end_time': forms.TimeInput(
                attrs={'class': 'form-control form-control-lg', 'type': 'time', 'min': '08:00', 'max': '22:00'}),
            'location': forms.Textarea(attrs={'class': 'form-control form-control-lg'}),
            'color': forms.Select(attrs={'class': 'form-control form-control-lg'}),
            'link': forms.Textarea(attrs={'class': 'form-control form-control-lg'}),
            'zoom_password': forms.TextInput(attrs={'class': 'form-control form-control-lg'})
        }

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            kwargs['initial'] = {
                'weekday': ast.literal_eval(kwargs.get('instance').weekday or '[]'),
            }

        # Defines the user from the kwargs to prevent the multiple values error
        user = kwargs.pop('user', None)
        super(CourseTimeEditForm, self).__init__(*args, **kwargs)
        # Changes the user from the default to the request
        self.fields['course'].queryset = Course.objects.filter(user=user)
        for visible in self.visible_fields():
            visible.field.widget.attrs['rows'] = '4'


class CourseFileForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(user=1),
        widget=forms.Select(attrs={'class': 'form-control form-control-lg'})
    )

    class Meta:
        model = CourseFile
        exclude = ['uploaded']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'style': 'width: 100%'}),
        }

    def __init__(self, *args, **kwargs):
        # Defines the user from the kwargs to prevent the multiple values error
        user = kwargs.pop('user', None)
        super(CourseFileForm, self).__init__(*args, **kwargs)
        # Changes the user from the default to the request
        self.fields['course'].queryset = Course.objects.filter(user=user)
        for visible in self.visible_fields():
            visible.field.widget.attrs['rows'] = '4'

class CourseLinkForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(user=1),
        widget=forms.Select(attrs={'class': 'form-control form-control-lg'})
    )

    class Meta:
        model = CourseLink
        exclude = ['uploaded']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'link': forms.URLInput(attrs={'class': 'form-control form-control-lg'}),
        }

    def __init__(self, *args, **kwargs):
        # Defines the user from the kwargs to prevent the multiple values error
        user = kwargs.pop('user', None)
        super(CourseLinkForm, self).__init__(*args, **kwargs)
        # Changes the user from the default to the request
        self.fields['course'].queryset = Course.objects.filter(user=user)
        for visible in self.visible_fields():
            visible.field.widget.attrs['rows'] = '4'


class FeedbackForm(forms.Form):
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-lg'}), label='Message')
