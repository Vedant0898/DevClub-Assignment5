from django.contrib import admin

from .models import DiscussionForum,Announcement,Message
# Register your models here.

admin.site.register(DiscussionForum)
admin.site.register(Announcement)
admin.site.register(Message)