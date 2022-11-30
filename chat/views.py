from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse
from django.http import HttpResponseRedirect
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


def contacts(request):
    pass

def chat_room(request):
    pass

def auth_user(request):
    pass