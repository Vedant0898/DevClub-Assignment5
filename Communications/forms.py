from django import forms

from .models import Message,Announcement,DiscussionForum

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

class DiscussionForumForm(forms.ModelForm):
    """form for discussion"""

    class Meta:
        model = DiscussionForum
        exclude = ('sender','is_pinned','course',)
    def __init__(self, course, *args, **kwargs):
        super(DiscussionForumForm, self).__init__(*args, **kwargs)
        self.fields['reply_to'].queryset = DiscussionForum.objects.filter(course=course)