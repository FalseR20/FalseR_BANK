from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *


# Главная страница
def index(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            client = Clients.objects.get(user=request.user.id)
            return render(
                request, "index.html",
                {
                    "user": request.user.get_username,
                    "cards": Cards.objects.filter(client=client)
                }
            )
        else:
            return render(request, "base.html")
    else:
        return render(request, "guest.html")


# Регистрация
def log_up(request):
    if request.method == "POST":
        user_form = UserRegistration(request.POST)
        if not user_form.is_valid():
            return render(request, "index.html",
                          {"user": "самый умный? Давай нормально регайся и оформляй кредитик"})
        else:
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            if password == confirm_password:
                username = request.POST.get("username")
                user = User(username=username)
                user.set_password(password)  # с хешированием
                user.save()

                fullname = request.POST.get("fullname")
                client = Clients(fullname=fullname)
                client.user = user
                client.save()

                login(request, user)
                return HttpResponseRedirect("/")

    user_form = UserRegistration()
    return render(request, "registration/logup.html", {"title": "Sign Up", "form": user_form})


# Вход
def log_out(request):
    logout(request)
    return HttpResponseRedirect("/")


# Привязка карт
def cards(request):
    return render(request, "cards.html")
