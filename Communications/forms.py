from django import forms

from .models import Message,Announcement

class MessageForm(forms.ModelForm):
    """form for sending DM"""

    class Meta:
        model = Message
        exclude = ('sender',)

class AnnouncementForm(forms.ModelForm):
    """form for announcement"""

    class Meta:
        model = Announcement
        exclude= ('course','instructor',)
        label = {
            'is_pinned':'Pin this announcement',
        }
