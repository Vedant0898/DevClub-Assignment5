from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Instructor(models.Model):
    """Model for Instructor"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    verification_status = models.BooleanField()

    def __str__(self):
        s = f'{self.user} ({self.email})'
        return s

class Student(models.Model):
    """Model for Student"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        s = f'{self.user} ({self.email})'
        return s

class Course(models.Model):
    """Model for Course"""
    year = models.IntegerField()
    sem = models.IntegerField()

    subject = models.CharField(max_length=3)
    course_code = models.IntegerField()
    course_description = models.CharField(max_length=50)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)

    course_status = (
        ('1','Ongoing'),
        ('2','Completed')
    )

    status = models.CharField(max_length=1, choices=course_status,default='1')
    class Meta:
       ordering = ['-year', '-sem', 'subject','course_code']

    def __str__(self):
        s = f'{self.year}-{self.sem} {self.subject}{self.course_code}'
        return s

class Participants(models.Model):
    """Model for participants of course"""

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    verification_status = models.BooleanField()

    class Meta:
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'
        ordering = ['course']

    def __str__(self):
        s = f'{self.course.subject}{self.course.course_code} # {self.student.user}'
        return s