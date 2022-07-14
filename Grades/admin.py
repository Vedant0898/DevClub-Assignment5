from django.contrib import admin
from .models import Grade, Assignment, AssignmentSubmission

# Register your models here.

admin.site.register(Grade)
admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)