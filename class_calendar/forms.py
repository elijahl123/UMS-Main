from django import forms

from class_calendar.models import CalendarEvent


class AddEvent(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        exclude = ['uid']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control form-control-lg', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control form-control-lg', 'type': 'time'}),
            'title': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': '4'}),
        }
