from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from Users.models import Course, Student, Instructor, Participants
from .models import Grade, Assignment, AssignmentSubmission
from .forms import AssignmentForm,AssignmentSubmissionForm
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

@login_required
def view_all_assignments(request,course_id):
    """Displays all assignments of a given course"""

    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))

    course = get_object_or_404(Course,id=course_id)
    context = {'course':course,'is_instructor':False, 'registered':False}
    if request.session['role'] == 'instructor':
        instr = Instructor.objects.get(user=request.user)
        if course.instructor != instr:
            return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

        context['is_instructor'] = True
        context['registered']=True
    
    elif request.session['role']=='student':

        stu = Student.objects.get(user=request.user)
        
        try:
            pt = Participants.objects.get(student=stu,course=course)
        except:
            return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

        context['registered'] = True

    assignments = course.assignment_set.all()

    context['assignments'] = assignments
    
    return render(request,'Grades/view_all_assignments.html',context=context)


@login_required
def view_assignment(request,assignment_id):
    """Displays details of a assignment"""

    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))

    assnment = Assignment.objects.get(id = assignment_id)
    course = assnment.course

    context = {'a':assnment,'a_sub':None,'course':course,'is_instructor':False, 'registered':False}
    if request.session['role'] == 'instructor':
        instr = Instructor.objects.get(user=request.user)
        if course.instructor != instr:
            return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

        context['is_instructor'] = True
        context['registered']=True
    
    elif request.session['role']=='student':

        stu = Student.objects.get(user=request.user)
        
        try:
            pt = Participants.objects.get(student=stu,course=course)
        except:
            return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

        context['registered'] = True

        try:
            a_sub=AssignmentSubmission.objects.get(assignment=assnment,student=stu)
            context['a_sub']=a_sub
        except:
            pass
    return render(request,'Grades/view_assignment.html',context=context)

    
@login_required
def edit_assignment(request,assignment_id):
    """Instructor can edit a current assignment"""

    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))

    assnment = Assignment.objects.get(id = assignment_id)
    course = assnment.course

    if request.session['role'] == 'instructor':
        instr = Instructor.objects.get(user=request.user)
        if course.instructor != instr:
            return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})
    
    else:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    if request.method != 'POST':
        form = AssignmentForm(instance = assnment)
    
    else:
        form = AssignmentForm(instance=assnment, data=request.POST,files=request.FILES)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('Grades:view_assignment',args=[assnment.id]))
    
    context = {'a':assnment,'course':course,'form':form}


    return render(request,'Grades/edit_assignment.html',context=context)

@login_required
def create_assignment(request,course_id):
    """Instructor can create a new assignment for given course"""

    
    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))

    course = get_object_or_404(Course,id=course_id)

    if request.session['role'] == 'instructor':
        instr = Instructor.objects.get(user=request.user)
        if course.instructor != instr:
            return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})
    
    else:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    if request.method != 'POST':
        form = AssignmentForm()
    
    else:
        form = AssignmentForm(data=request.POST,files=request.FILES)

        if form.is_valid():
            new_assignment = form.save(commit=False)
            new_assignment.course = course

            new_assignment.save()

            return HttpResponseRedirect(reverse('Grades:all_assignments',args=[course.id]))
    
    context = {'course':course,'form':form}


    return render(request,'Grades/create_assignment.html',context=context)

@login_required
def delete_assignment(request,assignment_id):
    """Instructor can delete existing assignments"""

    
    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))

    assnment = Assignment.objects.get(id = assignment_id)
    course = assnment.course

    if request.session['role'] == 'instructor':
        instr = Instructor.objects.get(user=request.user)
        if course.instructor != instr:
            return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})
    
    else:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    # print(assnment, 'deleted successfully')
    assnment.delete()

    return HttpResponseRedirect(reverse('Grades:all_assignments',args=[course.id]))

@login_required
def submit_assignment(request,assignment_id):
    """Student can submit assignment"""

    
    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))
    
    if not check_student(request):
        return HttpResponseRedirect(reverse('Users:index'))
    
    stu = Student.objects.get(user = request.user)
    assnment = Assignment.objects.get(id = assignment_id)

    try:
        pt = Participants.objects.get(course = assnment.course,student=stu)
    except:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    if request.method!='POST':
        # display new form
        form = AssignmentSubmissionForm()
    
    else:
        form = AssignmentSubmissionForm(data = request.POST,files = request.FILES)

        if form.is_valid():
            new_submission = form.save(commit=False)

            new_submission.student = stu
            new_submission.assignment = assnment

            new_submission.save()

            return HttpResponseRedirect(reverse('Grades:view_assignment',args=[assignment_id]))

    context = {'form':form,'a':assnment}

    return render(request,'Grades/submit_assignment.html',context=context)


@login_required
def resubmit_assignment(request,assignment_id):
    """Student can REsubmit assignment"""

    
    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))
    
    if not check_student(request):
        return HttpResponseRedirect(reverse('Users:index'))
    
    stu = Student.objects.get(user = request.user)
    assnment = Assignment.objects.get(id = assignment_id)
    
    try:
        a_sub = AssignmentSubmission.objects.get(assignment = assnment, student = stu )
    except:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    try:
        pt = Participants.objects.get(course = a_sub.assignment.course,student=stu)
    except:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    if request.method!='POST':
        # display new form
        form = AssignmentSubmissionForm(instance = a_sub)
    
    else:
        form = AssignmentSubmissionForm(data = request.POST,files = request.FILES,instance = a_sub)

        if form.is_valid():
            form.save()

            if len(request.FILES)==0:
                a_sub.delete()

            return HttpResponseRedirect(reverse('Grades:view_assignment',args=[assignment_id]))

    context = {'form':form,'a_sub':a_sub,'a':assnment}

    return render(request,'Grades/resubmit_assignment.html',context=context)