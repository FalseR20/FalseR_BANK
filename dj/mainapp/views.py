import datetime
import random

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from .functions import *


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
    accounts = (tuple((account.iban, f"{account.iban} ({account.currency.code})") for account in
                      Accounts.objects.filter(clients=client)) +
                tuple((str(-currency.id), f"New account in {currency.code}") for currency in Currencies.objects.all()))
    card_form = CardForm(account_choices=accounts, cardholder_name=client.fullname.upper())

    if request.method == "POST":
        system_post = int(request.POST.get("system"))
        time_post = int(request.POST.get("time"))
        cardholder_name = request.POST.get("cardholder_name").upper()
        account_post = request.POST.get("account")

        # Validation
        in_system = [el[0] for el in card_form.fields['system'].choices]
        in_time = range(1, 6)
        in_account = [el[0] for el in accounts]
        if system_post in in_system and time_post in in_time and account_post in in_account:
            # Addition stage
            if account_post[0] == '-':
                account_post = -int(account_post)
                last_acc = Accounts.objects.last()
                print(last_acc)
                account = client.accounts_set.create(
                    iban=make_iban(Currencies.objects.get(id=account_post).code,
                                   "1",
                                   ("%016d" % (int(last_acc.iban[12:]) + 1)) if last_acc else "0000000000000000"),
                    currency_id=account_post,
                    balance=0,
                    iz_freeze=False).save()
            else:
                account = Accounts.objects.get(iban=account_post)
            last_card = Cards.objects.last()
            new_card = Cards.objects.create(
                number=int(str(system_post) +
                           "23814" +
                           (("%010d" % (last_card.number % 1e10 + 1)) if last_card else "0000000000")),
                client=client,
                account=account,
                cardholder_name=cardholder_name,
                expiration_date=datetime.date(year=datetime.datetime.now().year + time_post,
                                              month=datetime.datetime.now().month,
                                              day=31),
                security_code=random.randint(1, 999),
                iz_freeze=False).save()
            return redirect('/')

    return render(request, "cards.html", {'form': card_form})
