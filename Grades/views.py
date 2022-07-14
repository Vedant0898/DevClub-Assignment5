from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required

from Users.models import Course, Student
from .models import Grade
# Create your views here.


def check_instructor(request):
    """returns true if the user is instructor else false"""

    if 'role' not in request.session:
        return False
    if request.session['role']!='instructor':
        return False
    
    return True


def check_student(request):
    """returns true if the user is student else false"""

    if 'role' not in request.session:
        return False
    if request.session['role']!='student':
        return False
    
    return True
    

@login_required
def course_grade(request,course_id):
    """display grade of student(request user) of given course"""
    if not check_student(request):
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    course = get_object_or_404(Course,id=course_id)
    stu = Student.objects.get(user=request.user)
    grade_available = True
    grade = None
    try:
        grade = Grade.objects.get(course=course, student=stu)
    except:
        grade_available = False
    context = {'grade':grade,'course':course,'student':stu,'grade_available':grade_available}

    return render(request, 'Grades/course_grade.html',context=context)
