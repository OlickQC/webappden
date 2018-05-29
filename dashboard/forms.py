from .models import Notes
from django import forms
from django.forms import ModelForm

class NoteForm(ModelForm):
    note = forms.models.Field(help_text="Entrez une note", required=False)
    class Meta:
        model = Notes
        fields = ('note',)