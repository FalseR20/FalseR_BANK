import datetime
import random

from django.shortcuts import render, redirect
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
                    "user": request.user.get_username(),
                    "cards": Cards.objects.filter(client=client),
                    "accounts": Accounts.objects.filter(clients=client),
                }
            )
        else:
            return render(request, "base.html", {"staff_user": request.user.get_username()})
    else:
        return render(request, "guest.html")


# Регистрация
def sign_up(request):
    if request.method == "POST":
        user_form = UserRegistration(request.POST)
        if user_form.is_valid():
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
    return render(request, "registration/signup.html", {"form": user_form})


# Вход
def sign_out(request):
    logout(request)
    return HttpResponseRedirect("/")


# Привязка карт
def cards(request):
    client = Clients.objects.get(user=request.user.id)
    accounts = (tuple((account.id, f"{account.id} ({account.currency.code})") for account in
                      Accounts.objects.filter(clients=client)) +
                tuple((-currency.id, f"New account in {currency.code}") for currency in Currencies.objects.all()))
    card_form = CardForm(account_choices=accounts, cardholder_name=client.fullname.upper())

    if request.method == "POST":
        system_post = int(request.POST.get("system"))
        time_post = int(request.POST.get("time"))
        cardholder_name = request.POST.get("cardholder_name").upper()
        account_post = int(request.POST.get("account"))

        # Validation
        in_system = [el[0] for el in card_form.fields['system'].choices]
        in_time = range(1, 6)
        in_account = [el[0] for el in accounts]
        if system_post in in_system and time_post in in_time and account_post in in_account:
            if account_post < 0:
                account = client.accounts_set.create(currency_id=-account_post, balance=0)
                account.save()
            else:
                account = Accounts.objects.get(id=account_post)

            new_card = Cards.objects.create(number=str(system_post) + "22820" + str(Cards.objects.last().number + 1)[6:],
                                            client=client,
                                            account=account,
                                            cardholder_name=cardholder_name,
                                            expiration_date=datetime.date(year=datetime.datetime.now().year + time_post,
                                                                          month=datetime.datetime.now().month,
                                                                          day=31),
                                            security_code=random.randint(1, 999))
            new_card.save()
            return redirect('/')

    return render(request, "cards.html", {'form': card_form})
