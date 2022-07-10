from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course


# Create your views here.
def index(request):
    return render(request,'Users/index.html')

def courses(request,course_name):
    sub = course_name[:3]
    num = 0
    if(len(course_name)>3):
        num = course_name[-3:]
    
    course = Course.objects.get(subject__contains = sub, course_code__contains=num)
    context = {'course':course}
    return render(request,'Users/course_desc.html',context=context)


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
    del request.session['role']
    logout(request)
    return HttpResponseRedirect(reverse('Users:index'))