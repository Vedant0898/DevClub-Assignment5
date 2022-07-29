from django import forms

from .models import Docs

class DocForm(forms.ModelForm):
    class Meta:
        model = Docs
        exclude = ('course',)
