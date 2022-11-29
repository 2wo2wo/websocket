from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse
from django.http import HttpResponseRedirect
# Create your views here.

def index(request):
    return render(request, 'chat/index.html')