from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date

from .models import Course,Instructor
from .forms import CourseForm


# Create your views here.
def index(request):
    return render(request,'Users/index.html')

def course(request,course_id):
    course = Course.objects.get(id=course_id)
    context = {'course':course}
    return render(request,'Users/course_desc.html',context=context)


def courses(request):
    courses = Course.objects.all().order_by('-id')
    context = {'courses':courses,'is_instructor':False}
    if 'role' in request.session and request.session['role']=='instructor':
        context['is_instructor'] = True

    return render(request,'Users/view_all_courses.html',context=context)

def login_user(request):
    if request.method!='POST':
        #Display a login form
        form = AuthenticationForm(request)
    
    else:
        #process completed form
        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request,user)
            if (user.student_set.all().exists()):
                request.session['role'] = 'student'
            elif (user.instructor_set.all().exists()):
                request.session['role'] = 'instructor'
            
            return HttpResponseRedirect(reverse('Users:index'))

    context = {'form':form}
    return render(request,'Users/login.html',context=context)

def logout_user(request):
    if 'role' in request.session:
        del request.session['role']
    logout(request)
    return HttpResponseRedirect(reverse('Users:index'))

@login_required
def register_new_course(request):
    # Handle auth logic
    if 'role' not in request.session:
        return render(request,'Users/error.html',{'error':"You are not authorised to access this page"})
    if request.session['role']!='instructor':
        return render(request,'Users/error.html',{'error':"You are not authorised to access this page"})
    
    instr = Instructor.objects.get(user=request.user)
    if request.method != 'POST':
        # Create a form with some prefilled data
        data = {'year': date.today().year}
        form = CourseForm(initial=data)

    else:
        #Process filled form
        form = CourseForm(request.POST)

        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = instr
            course.save()
            return HttpResponseRedirect(reverse('Users:courses'))
        else:
            print('some error')
    context = {'form' : form}



    return render(request,'Users/register_new_course.html',context=context)