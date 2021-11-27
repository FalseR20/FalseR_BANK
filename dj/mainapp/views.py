from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *


# Главная страница
def index(request):
    if request.user.is_authenticated:
        return render(request, "index.html", {"user": request.user.get_username})
    else:
        return render(request, "index.html", {"user": "Anonymous"})


# сохранение пользователей
def log_up(request):
    if request.method == "POST":
        user_form = UserRegistration(request.POST)
        if not user_form.is_valid():
            return render(request, "index.html",
                          {"user": "самый умный? Давай нормально регайся и оформляй кредитик"})
        else:
            username = request.POST.get("username")
            first_name = request.POST.get("first_name")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            if password == confirm_password:
                user = User(
                    username=username,
                    first_name=first_name,
                    password=password
                )
                user.save()
                login(request, user)
                return HttpResponseRedirect("/")

    user_form = UserRegistration()
    return render(request, "registration/login.html", {"title": "Sign Up", "form": user_form})


def log_out(request):
    logout(request)
    return HttpResponseRedirect("/")
