from django import forms

from .models import Message

class MessageForm(forms.ModelForm):
    """form for sending DM"""

    class Meta:
        model = Message
        exclude = ('sender',)