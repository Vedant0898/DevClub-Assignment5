from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.urls import reverse
import statistics

from Users.models import Course, Student, Instructor, Participants
from .models import Grade, Assignment, AssignmentSubmission
from .forms import AssignmentForm,AssignmentSubmissionForm, AssignmentGradingForm
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

def get_stats(data):
    if len(data)==0:
        return None
    if len(data)==1:
        stats = {
            'mean':data[0],
            'median':data[0],
            'max':data[0],
            'stdev':0
        }
        return stats
    data.sort()
    mean = statistics.mean(data)
    median = statistics.median(data)
    maximum = max(data)
    stdev = statistics.stdev(data,mean)

    stats = {
        'mean':round(mean,2),
        'median':round(median,2),
        'max':round(maximum,2),
        'stdev':round(stdev,2)
        }
    
    return stats


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


@login_required
def grade_assignment(request,a_sub_id):
    """Instructor can grade an assignment"""

    
    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))
    
    if not check_instructor(request):
        return HttpResponseRedirect(reverse('Users:index'))
    
    instr = Instructor.objects.get(user=request.user)
    a_sub = AssignmentSubmission.objects.get(id=a_sub_id)

    if a_sub.assignment.course.instructor!=instr:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})


    if request.method != 'POST':
        form = AssignmentGradingForm(instance=a_sub)
    
    else:
        form = AssignmentGradingForm(data = request.POST, instance=a_sub)

        if form.is_valid():
            grade = form.save(commit=False)
            grade.is_graded = True
            if (grade.marks_obtained>a_sub.assignment.maximum_marks):
                grade.marks_obtained = a_sub.assignment.maximum_marks
            elif grade.marks_obtained<0:
                grade.marks_obtained=0
            grade.save()

            return HttpResponseRedirect(reverse('Grades:view_all_assignment_submission',args=[a_sub.assignment.id]))
    context = {'form':form,'a_sub':a_sub,'a':a_sub.assignment}
    
    return render(request,'Grades/grade_assignment.html',context=context)


@login_required
def view_all_assignment_submission(request,assignment_id):
    """View all graded and ungraded assignment submissions for instructor"""

    
    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))
    
    if not check_instructor(request):
        return HttpResponseRedirect(reverse('Users:index'))
    
    instr = Instructor.objects.get(user=request.user)
    assnment = Assignment.objects.get(id=assignment_id)

    if assnment.course.instructor!=instr:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    a_subs = assnment.assignmentsubmission_set.all()

    data = [sub.marks_obtained for sub in a_subs.filter(is_graded=True)]
    context = {'a':assnment,'a_subs':a_subs,'stats':get_stats(data)}
    return render(request,'Grades/view_all_assignment_submission.html',context = context)


@login_required
def calculate_total_grade(request,course_id):
    """Instructor can release total grade of a course"""

    
    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))
    
    if not check_instructor(request):
        return HttpResponseRedirect(reverse('Users:index'))
    
    instr = Instructor.objects.get(user=request.user)
    course = Course.objects.get(id=course_id)

    if course.instructor!=instr:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    pt = course.participants_set.all()
    assgnments = Assignment.objects.filter(course=course)
    den = sum([assmt.weightage for assmt in assgnments])

    if den==0:
        return render(request, 'Users/error.html',{'error':"No assignment found to grade."})

    a_subs_all = AssignmentSubmission.objects.filter(assignment__in = assgnments)

    for obj in pt:
        stu = obj.student
        
        a_subs = a_subs_all.filter(student=stu)
        num = sum([a_sub.marks_obtained*a_sub.assignment.weightage for a_sub in a_subs if a_sub.is_graded])

        try:
            g = Grade.objects.get(student=stu,course=course)
        except:
            g = Grade(student=stu,course = course)
        
        g.grade = round(num/den,2)

        g.save()
    
    #announcement to be added later
    
    return HttpResponseRedirect(reverse('Users:course',args=[course_id]))
    

@login_required
def view_total_grades_instr(request,course_id):
    """Instructor can view stats of all assignments of that course"""
    
    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))
    
    if not check_instructor(request):
        return HttpResponseRedirect(reverse('Users:index'))
    
    instr = Instructor.objects.get(user=request.user)
    course = Course.objects.get(id=course_id)

    if course.instructor!=instr:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    context = {'course':course,'ass_stats':None}

    assgnments = Assignment.objects.filter(course=course)
    ass_stats = {}
    total_weightage=0
    for ass in assgnments:
        a_subs = ass.assignmentsubmission_set.all()
        data = [sub.marks_obtained for sub in a_subs.filter(is_graded=True)]
        stats = get_stats(data)
        total_weightage+=ass.weightage
        ass_stats[ass]=stats
    
    grades = course.grade_set.all()
    data = [g.grade for g in grades if g.grade]
    g_stats = get_stats(data)
    context['ass_stats'] = ass_stats
    context['g_stats'] =  g_stats
    context['total_weightage'] = total_weightage
    return render(request,'Grades/view_grades_instr.html',context=context)

@login_required
def view_course_grade_student(request,course_id):
    """Student can view grade of a course"""

    
    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))
    
    if not check_student(request):
        return HttpResponseRedirect(reverse('Users:index'))
    
    stu = Student.objects.get(user = request.user)
    course = Course.objects.get(id = course_id)

    try:
        pt = Participants.objects.get(course = course,student=stu)
    except:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    context = {'course':course,'ass_stats':None}

    assgnments = Assignment.objects.filter(course=course)
    ass_stats = {}
    total_weightage=0
    for ass in assgnments:
        a_subs = ass.assignmentsubmission_set.all()     #all ass. sub. for this ass.
        data = [sub.marks_obtained for sub in a_subs.filter(is_graded=True)]
        stats = get_stats(data)
        try:
            stats['marks_obtained'] = a_subs.filter(student = stu)[0].marks_obtained
        except:
            pass
        total_weightage+=ass.weightage
        ass_stats[ass]=stats
    
    grades = course.grade_set.all()
    data = [g.grade for g in grades if g.grade]
    g_stats = get_stats(data)
    context['ass_stats'] = ass_stats
    context['g_stats'] =  g_stats
    context['total_weightage'] = total_weightage
    try:
        context['grade'] = grades.filter(student=stu)[0].grade
    except:
        pass
    return render(request,'Grades/view_course_grades_student.html',context=context)


@login_required
def view_all_grades_student(request):
    """Student can view grades for all registered courses"""

    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))
    
    if not check_student(request):
        return HttpResponseRedirect(reverse('Users:index'))
    
    stu = Student.objects.get(user = request.user)

    pt = Participants.objects.filter(student=stu)
    
    grade = {}
    for p in pt:
        try:
            g = Grade.objects.get(course = p.course,student=stu)
            grade[p.course] = g
        except:
            grade[p.course] = None
    
    context = {'s':stu,'grades':grade}
    print(context)

    return render(request,'Grades/view_all_grades_student.html',context=context)
