from django import forms

from notes.models import Note


class NotesForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ['uploaded', 'modified', 'course', 'user', 'uid']

