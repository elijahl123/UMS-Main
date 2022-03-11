from django import forms

from base.models import reminder_choices


class ReminderFormMixin(forms.Form):
    alert = forms.ChoiceField(
        choices=reminder_choices,
        widget=forms.Select(attrs={'class': 'form-control form-control-lg'}),
        initial=0
    )
    second_alert = forms.ChoiceField(
        choices=reminder_choices,
        widget=forms.Select(attrs={'class': 'form-control form-control-lg'}),
        initial=-1
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = [field for field in self.fields]
        fields.append(fields.pop(fields.index('alert')))
        fields.append(fields.pop(fields.index('second_alert')))
        self.order_fields(field_order=fields)


