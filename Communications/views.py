from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Announcement,DiscussionForum
from Users.models import Course,Student,Instructor,Participants
from .forms import MessageForm,AnnouncementForm, DiscussionForumForm
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
def view_dm(request):
    """View all sent and received dms for the user"""
    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))

    user = request.user
    received_messages = user.receiver.all()
    sent_messages = user.sender.all()

    context = {'user':user,'rm':received_messages,'sm':sent_messages}

    return render(request,'Communications/view_dm.html',context=context)


@login_required
def send_dm(request):
    """Send dm to any user"""
    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))

    user = request.user

    if request.method!='POST':
        form = MessageForm()
    
    else:
        form = MessageForm(data=request.POST)

        if form.is_valid():
            new_dm = form.save(commit=False)
            new_dm.sender = user
            new_dm.save()

            return HttpResponseRedirect(reverse('Comms:view_dm'))
    
    context = {'user':user,'form':form}

    return render(request,'Communications/send_dm.html',context=context)

@login_required
def view_all_announcements(request,course_id):
    """view all announcements for a given course"""

    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))

    course = Course.objects.get(id=course_id)
    context = {'is_instructor':False}

    if check_instructor(request):
        instr = Instructor.objects.get(user=request.user)
        if course.instructor!=instr:
            return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

        context['is_instructor']=True
    
    elif check_student(request):
        stu = Student.objects.get(user=request.user)
        try:
            pt = Participants.objects.get(student = stu,course=course)
        except:
            return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    
    else:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    anncments = Announcement.objects.filter(course=course)
    context['anc']=anncments
    context['course'] = course

    return render(request,'Communications/view_all_announcements.html',context=context)


@login_required
def view_announcement(request,anc_id):
    """view all announcements for a given course"""

    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))

    anc = Announcement.objects.get(id=anc_id)
    course = anc.course
    context = {'is_instructor':False}

    if check_instructor(request):
        instr = Instructor.objects.get(user=request.user)
        if course.instructor!=instr:
            return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

        context['is_instructor']=True
    
    elif check_student(request):
        stu = Student.objects.get(user=request.user)
        try:
            pt = Participants.objects.get(student = stu,course=course)
        except:
            return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    
    else:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    context['anc']=anc
    context['course'] = course

    return render(request,'Communications/view_announcement.html',context=context)

@login_required
def delete_announcement(request,anc_id):
    """Instructor can delete an announcement"""

    
    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))

    anc = Announcement.objects.get(id = anc_id)
    course = anc.course

    if request.session['role'] == 'instructor':
        instr = Instructor.objects.get(user=request.user)
        if course.instructor != instr:
            return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})
    
    else:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    
    anc.delete()

    return HttpResponseRedirect(reverse('Comms:view_all_announcements',args=[course.id]))



@login_required
def new_announcement(request,course_id):
    """Instructor can add a new announcement for given course"""

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
        form = AnnouncementForm()
    
    else:
        form = AnnouncementForm(data=request.POST)

        if form.is_valid():
            new_anc = form.save(commit=False)
            new_anc.course = course
            new_anc.instructor = instr

            new_anc.save()

            return HttpResponseRedirect(reverse('Comms:view_all_announcements',args=[course.id]))
    
    context = {'course':course,'form':form}


    return render(request,'Communications/new_announcement.html',context=context)



@login_required
def edit_announcement(request,anc_id):
    """Instructor can edit an existing announcement"""

    
    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))

    anc = Announcement.objects.get(id = anc_id)
    course = anc.course

    if request.session['role'] == 'instructor':
        instr = Instructor.objects.get(user=request.user)
        if course.instructor != instr:
            return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})
    
    else:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    if request.method != 'POST':
        form = AnnouncementForm(instance = anc)
    
    else:
        form = AnnouncementForm(instance=anc, data=request.POST,files=request.FILES)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('Comms:view_announcement',args=[anc.id]))
    
    context = {'anc':anc,'course':course,'form':form}


    return render(request,'Communications/edit_announcement.html',context=context)

@login_required
def view_discussion(request,course_id):
    """Show all messages in discussion forum of a given course"""

    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))

    course = Course.objects.get(id=course_id)
    context = {'is_instructor':False}

    if check_instructor(request):
        instr = Instructor.objects.get(user=request.user)
        if course.instructor!=instr:
            return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

        context['is_instructor']=True
    
    elif check_student(request):
        stu = Student.objects.get(user=request.user)
        try:
            pt = Participants.objects.get(student = stu,course=course)
        except:
            return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    else:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    discs = DiscussionForum.objects.filter(course=course)
    context['discs']=discs
    context['course'] = course

    return render(request,'Communications/view_discussion.html',context=context)


@login_required
def add_discussion(request,course_id):
    """Add new discussion in discussion forum of a given course"""

    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))

    course = Course.objects.get(id=course_id)
    context = {'is_instructor':False}

    if check_instructor(request):
        instr = Instructor.objects.get(user=request.user)
        if course.instructor!=instr:
            return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

        context['is_instructor']=True
    
    elif check_student(request):
        stu = Student.objects.get(user=request.user)
        try:
            pt = Participants.objects.get(student = stu,course=course)
        except:
            return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    else:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    
    if request.method!='POST':
        form = DiscussionForumForm(course=course)
    else:
        form = DiscussionForumForm(course=course,data=request.POST)

        if form.is_valid():
            new_disc = form.save(commit=False)
            new_disc.sender = request.user
            new_disc.course = course
            new_disc.save()

            return HttpResponseRedirect(reverse('Comms:view_discussion',args=[course_id]))

    context['course'] = course
    context['form'] = form

    return render(request,'Communications/add_discussion.html',context=context)



@login_required
def edit_discussion(request,disc_id):
    """Edit a discussion in discussion forum of a given course by 
    sender or instructor"""

    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))

    disc = DiscussionForum.objects.get(id = disc_id)
    course = disc.course
    context = {'is_instructor':False}

    if check_instructor(request):
        instr = Instructor.objects.get(user=request.user)
        if course.instructor!=instr:
            return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

        context['is_instructor']=True
    
    elif disc.sender==request.user:
        stu = Student.objects.get(user=request.user)
        try:
            pt = Participants.objects.get(student = stu,course=course)
        except:
            return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    else:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    
    if request.method!='POST':
        form = DiscussionForumForm(course=course,instance=disc)
    else:
        form = DiscussionForumForm(course=course,instance=disc,data=request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('Comms:view_discussion',args=[course.id]))

    context['course'] = course
    context['form'] = form
    context['disc'] = disc

    return render(request,'Communications/edit_discussion.html',context=context)

@login_required
def change_pin_status(request,disc_id):
    """Instructor can pin or unpin a discussion"""

    disc = DiscussionForum.objects.get(id = disc_id)
    course = disc.course

    if check_instructor(request):
        instr = Instructor.objects.get(user=request.user)
        if course.instructor!=instr:
            return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    else:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})


    if disc.is_pinned:
        disc.is_pinned = False
    else:
        disc.is_pinned = True
    
    disc.save()

    return HttpResponseRedirect(reverse('Comms:view_discussion',args=[course.id]))



@login_required
def delete_discussion(request,disc_id):
    """Instructor can delete an announcement"""

    
    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))

    disc = DiscussionForum.objects.get(id = disc_id)
    course = disc.course

    if request.session['role'] == 'instructor':
        instr = Instructor.objects.get(user=request.user)
        if course.instructor != instr:
            return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})
    
    else:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    
    disc.delete()

    return HttpResponseRedirect(reverse('Comms:view_discussion',args=[course.id]))

