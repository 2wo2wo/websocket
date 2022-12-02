from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse
from django.http import HttpResponseRedirect, HttpResponse
from .models import Contact, Message
# Create your views here.

def index(request):
    return render(request, 'chat/index.html')


def login_view(request):
    if request.method =="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request , user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'chat/login.html', {
                "message": "Invalid login or password"
            })
    return render(request, 'chat/login.html')


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'chat/login.html', {
        "message": "You logged out"
    })

@login_required(login_url='/login_user/')
def contacts(request):
    user = request.user
    contact = Contact.objects.get(contact_owner_id=user.id)
    user_contacts = contact.contact_id.all()

    value = {
        'username': user.first_name,
        'contacts': user_contacts
    }
    return render(request, 'chat/contacts.html', value)



@login_required(login_url='/login_user/')
def chat_room(request, contact_id, user_id):
    right_messages = Message.objects.filter(sent_id=contact_id).filter(owner_id=user_id)
    left_messages = Message.objects.filter(sent_id=user_id).filter(owner_id=contact_id)
    messages = right_messages | left_messages
    messages = sorted(messages, key=lambda x: x.time_created)
    values = {
        'user_id': request.user.id,
        'messages': messages
    }
    return render(request, 'chat/chat_room.html', values)

def auth_user(request):
    pass