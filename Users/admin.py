from django.contrib import admin
from .models import Instructor, Student, Course, Participants

# Register your models here.

admin.site.register(Instructor)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Participants)