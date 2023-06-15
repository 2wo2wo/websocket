from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse
from django.http import HttpResponseRedirect, HttpResponse
from .models import Contact, Message, Unique_room
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .decorators import auth_user_chat_room, contacts_exists
# Create your views here.


def index(request):
    return render(request, 'chat/index.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
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
@contacts_exists
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


def user_exists(username):
    try:
        user = User.objects.get(username=username)
        return user
    except User.DoesNotExist:
        return 0


def contact_added(typed_user, user):
    user_contact = Contact.objects.get(contact_owner_id=user)
    user_contact.contact_id.add(typed_user)
    user_contact.save()


@login_required(login_url='/login_user/')
@contacts_exists
def contact_add(request):
    if request.method == 'POST':
        username = request.POST['username']
        typed_user = user_exists(username)
        if not typed_user:
            value = {
                'message': 'user does not exist'
            }
            return render(request, 'chat/contact_add.html', value)
        if typed_user != request.user:
            contact_added(typed_user, request.user)
        else:
            value = {
                'message': 'username are used'
            }
            return render(request, 'chat/contact_add.html', value)
        return HttpResponseRedirect(reverse('contacts'))
    return render(request, 'chat/contact_add.html')


def search_by_key(keyword):
    usernames = User.objects.filter(username__contains=keyword)
    first = User.objects.filter(first_name__contains=keyword)
    last = User.objects.filter(last_name__contains=keyword)
    email = User.objects.filter(email__contains=keyword)
    return usernames | first | last | email
    # return usernames


@login_required(login_url='/login_user/')
@contacts_exists
def contact_add_page(request):
    if request.method == "POST":
        results_search = search_by_key(request.POST['keyword'])
        if not len(results_search):
            value = {
                'message': 'Users not found. Can you try one more time?'
            }
            return render(request, 'chat/searchbar.html', value)
        if len(results_search) > 0:
            value = {
                "users": results_search
            }
            return render(request, 'chat/searchbar.html', value)
    return render(request, 'chat/searchbar.html')



@login_required(login_url='/login_user/')
@contacts_exists
def friend_add_function(request, user_id):
    user_contact = Contact.objects.get(contact_owner_id=request.user)
    friend = User.objects.get(pk=user_id)
    user_contact.contact_id.add(friend)
    user_contact.save()
    value = {
        'message': 'Friend added check contacts page'
    }
    return render(request, 'chat/searchbar.html', value)
