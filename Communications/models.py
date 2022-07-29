from django.db import models
from django.contrib.auth.models import User

from Users.models import Course,Instructor
# Create your models here.

class DiscussionForum(models.Model):
    """Discussion forum for a course"""
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    time_posted = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)

    class Meta:
        ordering = ['is_pinned','-time_posted']

    def __str__(self):
        return f'{self.text[:30]}... ({self.sender}) @ {self.course}'
    

class Announcement(models.Model):
    """Announcements for a course"""

    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    time_posted = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)

    class Meta:
        ordering = ['is_pinned','-time_posted']

    def __str__(self):
        return f'{self.text[:30]}... ({self.instructor}) @ {self.course}'

class Message(models.Model):
    """1-1 message"""

    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver')
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    title = models.CharField(max_length=200)
    text = models.TextField()
    time_sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time_sent']
    
    def __str__(self):
        return f'{self.text[:30]}... ({self.sender}) @ {self.receiver}'
