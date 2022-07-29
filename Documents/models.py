from django.db import models
import os
from uuid import uuid4

from Users.models import Course
from DevClubLMS import settings
# Create your models here.

class Docs(models.Model):
    """model for uploading course material"""

    def file_upload_path(instance,filename):
        ext = filename.split('.')[-1]
        new_name = f'{uuid4().hex}.{ext}'
        path = os.path.join(settings.MEDIA_ROOT,'course_materials',str(instance.course.id),new_name)
        return path

    # id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)

    doc = models.FileField(upload_to=file_upload_path)
    display_name = models.CharField(default = 'Document',max_length=100)
    notes = models.TextField(blank=True,null=True)

    class Meta:
        verbose_name = 'Doc'
        verbose_name_plural = 'Docs'

    def __str__(self):
        return f'{self.id}({self.display_name}) | {self.course}'

