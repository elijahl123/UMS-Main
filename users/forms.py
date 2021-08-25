from django.forms import forms, ModelForm

from users.models import Account


class AccountForm(ModelForm):
    class Meta:
        model = Account
        exclude = ['password', 'is_active', 'is_admin', 'is_staff', 'is_superuser']

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'
            visible.field.widget.attrs['style'] = 'border-width: 3px'