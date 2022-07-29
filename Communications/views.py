from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Message
from .forms import MessageForm
# Create your views here.

@login_required
def view_dm(request):
    if 'registration_incomplete' in request.session:
        return HttpResponseRedirect(reverse('Users:index'))

    user = request.user
    received_messages = user.receiver.all()
    sent_messages = user.sender.all()

    context = {'user':user,'rm':received_messages,'sm':sent_messages}

    return render(request,'Communications/view_dm.html',context=context)


@login_required
def send_dm(request):
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

