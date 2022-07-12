from django.shortcuts import render,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date

from .models import Course,Instructor,Student,Participants
from .forms import CourseForm



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
    

# Create your views here.
def index(request):
    return render(request,'Users/index.html')

def course(request,course_id):
    course = Course.objects.get(id=course_id)
    context = {'course':course,'is_instructor':False,'can_register':False}
    if check_instructor(request):
        instr = Instructor.objects.get(user=request.user)
        if course.instructor==instr:
            context['is_instructor'] = True
    
    if check_student(request):
        student = Student.objects.get(user = request.user)
        try:
            Participants.objects.get(course=course,student=student)
        except:
            context['can_register'] = True

    return render(request,'Users/course_desc.html',context=context)


def courses(request):
    courses = Course.objects.all()
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
def create_new_course(request):
    # Handle auth logic
    if not check_instructor(request):
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
        
    context = {'form' : form}



    return render(request,'Users/create_new_course.html',context=context)

@login_required
def edit_course(request,course_id):
    """Allows instructor to edit their own courses"""
    if not check_instructor(request):
        return render(request,'Users/error.html',{'error':"You are not authorised to access this page"})

    instr = Instructor.objects.get(user=request.user)
    course = get_object_or_404(Course,id=course_id)

    if course.instructor!=instr:
        return render(request,'Users/error.html',{'error':"You are not authorised to access this page"})

    if request.method !='POST':
        form = CourseForm(instance=course)
    
    else:
        form = CourseForm(instance=course, data=request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('Users:course',args=[course.id]))
    
    context = {'form': form,'course':course}

    return render(request,'Users/edit_course.html',context=context)

@login_required
def my_courses(request):
    #create 2 separate templates for student and non student
    if 'role' not in request.session:
        courses = Course.objects.all()
    elif request.session['role']=='student':
        stu = Student.objects.get(user = request.user)
        participants = Participants.objects.filter(student=stu)
        context = {'pt':participants}
        return render(request,'Users/view_my_courses_student.html',context=context)
    elif request.session['role']=='instructor':
        instr = Instructor.objects.get(user = request.user)
        courses = instr.course_set.order_by('-id')
    else:
        courses = Course.objects.all()
    
    context = {'courses':courses,'is_instructor':False}
    if 'role' in request.session and request.session['role']=='instructor':
        context['is_instructor'] = True

    return render(request,'Users/view_my_courses.html',context=context)

@login_required
def register_for_course(request,course_id):
    if not check_student(request):
        return render(request,'Users/error.html',{'error':"You are not authorised to access this page"})
    
    course = get_object_or_404(Course,id=course_id)
    student = Student.objects.get(user = request.user)
    try:
        Participants.objects.get(course = course, student = student)
        return render(request,'Users/error.html',{'error':"You are already registered for this course"})
    
    except:
        Participants.objects.create(course=course, student=student)

    return HttpResponseRedirect(reverse('Users:my_courses'))