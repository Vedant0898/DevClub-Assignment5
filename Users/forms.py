from django import forms

from .models import Course,Student,Instructor

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('instructor','status',)

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ('user',)

class InstructorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Instructor
        exclude = ('user','verification_status',)