from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required(login_url="accounts:sign-in")
def home(request):
    context = {}
    return render(request, "home/home.html",context)
