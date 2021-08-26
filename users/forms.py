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
        exclude = ['password', 'is_active', 'is_admin', 'is_staff', 'is_superuser', 'show_schedule_on_calendar']

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'
            visible.field.widget.attrs['style'] = 'border-width: 3px'


class AccountSettings(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['show_schedule_on_calendar']
        widgets = {
            'show_schedule_on_calendar': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
