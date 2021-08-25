from django.forms import ModelForm

from models import School


class SchoolForm(ModelForm):
    class Meta:
        model = School
        exclude = []

    def __init__(self, *args, **kwargs):
        super(SchoolForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'
            visible.field.widget.attrs['rows'] = '4'
            visible.field.widget.attrs['placeholder'] = ' '
