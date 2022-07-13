from django.shortcuts import render,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date

from .models import Course,Instructor,Student,Participants
from .forms import CourseForm, StudentRegistrationForm, InstructorRegistrationForm



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
    """Index page"""

    return render(request,'Users/index.html')

def course(request,course_id):
    """individual course description"""

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
    """view all courses"""

    courses = Course.objects.all()
    context = {'courses':courses,'is_instructor':False}
    if 'role' in request.session and request.session['role']=='instructor':
        context['is_instructor'] = True

    return render(request,'Users/view_all_courses.html',context=context)

def login_user(request):
    """Login user and set appropriate role"""

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Users:index'))

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
                instr = Instructor.objects.get(user=user)

                if instr.verification_status==False:
                    request.session['instr_not_verified'] = True

            elif not user.is_staff:
                request.session['registration_incomplete'] = True
            
            return HttpResponseRedirect(reverse('Users:index'))

    context = {'form':form}
    return render(request,'Users/login.html',context=context)

def logout_user(request):
    """Clear session and logout user"""

    if 'role' in request.session:
        del request.session['role']
    if 'registration_incomplete' in request.session:
        del request.session['registration_incomplete']
    if 'instr_not_verified' in request.session:
        del request.session['instr_not_verified']

    logout(request)
    return HttpResponseRedirect(reverse('Users:index'))

@login_required
def create_new_course(request):
    """Allow verified instructor to create new course"""
    
    if not check_instructor(request):
        return render(request,'Users/error.html',{'error':"You are not authorised to access this page"})

    if 'instr_not_verified' in request.session:
        return render(request,'Users/error.html',{'error':"You are not verified as an instructor"})
 
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

    if 'instr_not_verified' in request.session:
        return render(request,'Users/error.html',{'error':"You are not verified as an instructor"})

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
    """Displays the courses registered by student or the courses of instructor depending 
    on role of user"""

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
    """Allows student to register in course"""

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

def register_user(request):
    """New user registration step-1"""

    if request.user.is_authenticated and 'registration_incomplete' not in request.session:
        return HttpResponseRedirect(reverse('Users:index'))

    if request.method!='POST':
        # display a blank registration form
        form = UserCreationForm()
    else:
        # post data submitted
        form = UserCreationForm(data = request.POST)

        if form.is_valid():
            new_user = form.save()

            #log in the user
            authenticated_user = authenticate(username=new_user.username,password=request.POST['password1'])
            login(request,authenticated_user)
            request.session['registration_incomplete'] = True
            return HttpResponseRedirect(reverse('Users:register_user'))
    context = {'form': form}

    return render(request,'Users/register_user.html',context=context)

@login_required
def register_student(request):
    """New user registration step-2 for student"""

    if 'registration_incomplete' not in request.session:
        return HttpResponseRedirect(reverse('Users:index'))

    if request.method!='POST':
        #display blank form
        form = StudentRegistrationForm()
    
    else:
        # post data submitted
        form = StudentRegistrationForm(data=request.POST)

        if form.is_valid():
            new_student = form.save(commit=False)
            new_student.user = request.user

            new_student.save()
            
            del request.session['registration_incomplete']
            request.session['role'] = 'student'

            return HttpResponseRedirect(reverse('Users:index'))

    context = {'form':form}

    return render(request,'Users/register_student.html',context=context)

@login_required
def register_instructor(request):
    """New user registration step-2 for instructor"""

    if 'registration_incomplete' not in request.session:
        return HttpResponseRedirect(reverse('Users:index'))

    if request.method!='POST':
        #display blank form
        form = InstructorRegistrationForm()
    
    else:
        # post data submitted
        form = InstructorRegistrationForm(data=request.POST)

        if form.is_valid():
            new_instr = form.save(commit=False)
            new_instr.user = request.user

            new_instr.save()
            
            del request.session['registration_incomplete']
            request.session['role'] = 'instructor'
            request.session['instr_not_verified'] = True

            return HttpResponseRedirect(reverse('Users:index'))

    context = {'form':form}

    return render(request,'Users/register_instructor.html',context=context)

def view_profile(request,user_name):
    """profile page for users"""

    user = User.objects.get(username = user_name)

    if (user.student_set.all().exists()):
        #user is student
        stu = Student.objects.get(user = user)
        is_owner = False
        if request.user.is_authenticated and user==request.user:
            is_owner = True
        context = {'person':stu,'is_owner':is_owner}
        return render(request,'Users/profile_reg_users.html',context=context)

    elif (user.instructor_set.all().exists()):
        #user is instr
        # request.session['role'] = 'instructor'
        instr = Instructor.objects.get(user=user)
        is_owner = False
        if request.user.is_authenticated and user==request.user:
            is_owner = True
        context = {'person':instr,'is_owner':is_owner}
        return render(request,'Users/profile_reg_users.html',context=context)

    # else
    is_staff = False
    if user.is_staff:
        #reg incomplete
        is_staff = True
    is_owner = False
    if request.user.is_authenticated and user==request.user:
        is_owner = True
    context = {'is_owner':is_owner,'is_staff':is_staff,'person':user}
    return render(request,'Users/profile_other.html',context=context)


@login_required
def edit_profile(request):
    """edit profile for students and instructors"""

    if 'role' not in request.session or 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))
    
    if request.session['role']=='student':
        stu = Student.objects.get(user=request.user)

        if request.method != 'POST':
            form = StudentRegistrationForm(instance = stu)
        else:
            form = StudentRegistrationForm(instance=stu,data=request.POST)

            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('Users:view_profile',args=[request.user.username]))
        
        context = {'form':form,'person':stu}
        return render(request,'Users/edit_profile.html',context=context)
    
    elif request.session['role']=='instructor':
        instr = Instructor.objects.get(user=request.user)

        if request.method != 'POST':
            form = InstructorRegistrationForm(instance = instr)
        else:
            form = InstructorRegistrationForm(instance=instr,data=request.POST)

            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('Users:view_profile',args=[request.user.username]))
        
        context = {'form':form,'person':instr}
        return render(request,'Users/edit_profile.html',context=context)

    else:
        return HttpResponseRedirect(reverse('Users:index'))

def view_participants(request,course_id):
    """display participants of a given course"""

    course = get_object_or_404(Course, id = course_id)

    participants = course.participants_set.all()

    context = {'pt':participants,'course':course}

    return render(request,'Users/view_participants.html',context=context)