from django import forms

from users.models import Account

color_choices = [
    ('primary', 'Blue'),
    ('secondary', 'Gray'),
    ('success', 'Green'),
    ('danger', 'Red'),
    ('warning', 'Yellow'),
    ('info', 'Light Blue'),
]


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'send_scheduled_emails', 'homework_notifications', 'class_notifications']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'style': 'border-width: 3px'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'style': 'border-width: 3px'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'style': 'border-width: 3px'}),
            'send_scheduled_emails': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'homework_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'class_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AccountSettings(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['show_schedule_on_calendar', 'send_scheduled_emails', 'homework_notifications', 'class_notifications']
        widgets = {
            'show_schedule_on_calendar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'send_scheduled_emails': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'homework_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'class_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
