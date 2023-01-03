from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse
from django.http import HttpResponseRedirect, HttpResponse
from .models import Contact, Message, Unique_room
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from.decorators import auth_user_chat_room
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


def chat_room_name(contact_id, user_id):
    user1 = User.objects.get(pk=contact_id)
    user2 = User.objects.get(pk=user_id)
    try:
        room_id = Unique_room.objects.filter(users__in=[user1,]).get(users__in=[user2,])
        return room_id.id
    except ObjectDoesNotExist:
        room_id = Unique_room.objects.create()
        room_id.users.add(user1)
        room_id.users.add(user2)
        room_id.save()
        return room_id.id


@login_required(login_url='/login_user/')
@auth_user_chat_room
def chat_room(request, contact_id, user_id):
    right_messages = Message.objects.filter(sent_id=contact_id).filter(owner_id=user_id)
    left_messages = Message.objects.filter(sent_id=user_id).filter(owner_id=contact_id)
    messages = right_messages | left_messages
    messages = sorted(messages, key=lambda x: x.time_created)
    # room_name = str(contact_id) + '/' + str(user_id)
    # print(chat_room_name(contact_id, user_id))       # old version chat_room
    room_name = str(chat_room_name(contact_id, user_id))
    values = {
        'user_id': request.user.id,
        'room_name': room_name,
        'messages': messages
    }
    return render(request, 'chat/chat_room.html', values)


def auth_user(request):
    pass


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password_confirm = request.POST["confirm-password"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        if password == password_confirm:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password,
                                            last_name=last_name,
                                            first_name=first_name
                                            )

            user.save()
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'main/register.html', {
                "message": "passwords do not match"
            })

    return render(request, 'chat/registration.html')
