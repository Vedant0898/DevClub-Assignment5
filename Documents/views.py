from multiprocessing import context
from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from Users.models import Course,Student,Instructor,Participants
from .models import Docs
from .forms import DocForm
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
def view_all_docs(request,course_id):
    """Display all uploaded docs for the given course"""

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
    
    documents = course.docs_set.all()

    context['docs'] = documents

    return render(request,'Documents/view_all_docs.html',context=context)

@login_required
def delete_doc(request,doc_id):
    """Instructor can delete a doc"""

    
    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))

    if not check_instructor(request):
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})


    doc = Docs.objects.get(id = doc_id)
    course = doc.course

    instr = Instructor.objects.get(user=request.user)
    if course.instructor != instr:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})
    
    
    doc.delete()

    return HttpResponseRedirect(reverse('Docs:all_docs',args=[course.id]))


@login_required
def add_doc(request,course_id):
    """Instructor can add course material"""
    
    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))

    if not check_instructor(request):
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})


    course = Course.objects.get(id=course_id)
    instr = Instructor.objects.get(user=request.user)

    if course.instructor!=instr:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})
    
    if request.method!='POST':
        form = DocForm()
    
    else:
        form = DocForm(data=request.POST,files=request.FILES)

        if form.is_valid():
            new_doc = form.save(commit=False)
            new_doc.course=course
            new_doc.save()

            return HttpResponseRedirect(reverse('Docs:all_docs',args=[course.id]))
    
    context = {'course':course,'form':form}

    return render(request,'Documents/add_doc.html',context=context)


@login_required
def edit_doc(request,doc_id):
    """Instructor can edit course material"""
    
    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))

    if not check_instructor(request):
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})

    doc = Docs.objects.get(id=doc_id)
    course = doc.course
    instr = Instructor.objects.get(user=request.user)

    if course.instructor!=instr:
        return render(request, 'Users/error.html',{'error':"You are not authorised to access this page"})
    
    if request.method!='POST':
        form = DocForm(instance=doc)
    
    else:
        form = DocForm(instance=doc,data=request.POST,files=request.FILES)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('Docs:all_docs',args=[course.id]))
    
    context = {'course':course,'form':form,'doc':doc}

    return render(request,'Documents/edit_doc.html',context=context)

