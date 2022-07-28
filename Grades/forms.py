from django import forms
from django.contrib.admin import widgets

from .models import Assignment, AssignmentSubmission, Grade

class AssignmentForm(forms.ModelForm):
    """form for assignment creation/editing"""
    class Meta:
        model = Assignment
        exclude = ('course',)
        labels = {
            'start_date':'Start Date (in YYYY-MM-DD hh:mm:ss format)',
            'due_date':'Due Date (in YYYY-MM-DD hh:mm:ss format)'
        }

class AssignmentSubmissionForm(forms.ModelForm):
    """form for submitting assignment"""

    class Meta:
        model = AssignmentSubmission
        exclude = ('assignment','student','is_graded','marks_obtained',)

class AssignmentGradingForm(forms.ModelForm):
    """form for grading an assignment"""

    class Meta:
        model = AssignmentSubmission
        exclude = ('is_graded','assignment','student','file',)
