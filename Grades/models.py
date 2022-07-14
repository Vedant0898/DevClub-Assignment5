from django.db import models

from Users.models import Course,Student
# Create your models here.

class Grade(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    grade = models.DecimalField(blank=True,null=True, max_digits=5,decimal_places=2)

    def __str__(self):
        return f'{self.course} # {self.student}'

class Assignment(models.Model):

    assignment_name = models.CharField(max_length=50)

    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()

    info = models.TextField(blank=True,null=True)
    maximum_marks = models.IntegerField(default=100)
    weightage = models.DecimalField(default=100.0,max_digits=5,decimal_places=2)

    #submission related fields

    def __str__(self):
        return f'{self.assignment_name} - {self.course}'

    

class AssignmentSubmission(models.Model):

    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)

    submission_time = models.DateTimeField(auto_now_add=True)

    is_graded = models.BooleanField(default=False)
    marks_obtained = models.DecimalField(blank=True,null=True,max_digits=5,decimal_places=2)
    file = models.FileField(upload_to='assignment_submission/',blank=True,null=True)

    def __str__(self):
        return f'{self.assignment} ~ {self.student}'