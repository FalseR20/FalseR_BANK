import datetime
import random

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from .iban_func import make_iban


# Главная страница
def index(request):
    if not request.user.is_authenticated:
        return render(request, "guest.html")
    if not request.user.is_staff:
        client = Clients.objects.get(user=request.user.id)
        return render(
            request, "index.html",
            {
                "client": client,
                "cards": Cards.objects.filter(client=client),
                "accounts": Accounts.objects.filter(clients=client),
            }
        )
    return render(request, "base.html", {"staff_user": request.user})


# Регистрация
def sign_up(request):
    if request.method == "POST":
        user_form = UserRegistration(request.POST)
        if user_form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            if password == confirm_password and User.objects.filter(username=username).count() == 0:
                user = User(username=username)
                user.set_password(password)  # с хешированием
                user.save()

                fullname = request.POST.get("fullname")
                if fullname == "":
                    fullname = username
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
def new_card(request):
    if not request.user.is_authenticated and not request.user.is_staff:
        return HttpResponseRedirect("/")
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
                currency_id = -int(account_post)
                while True:
                    randiban = make_iban("1" + Currencies.objects.get(id=currency_id).code,
                                         "%016d" % random.randint(0, 9999_9999_9999_9999))
                    if not Accounts.objects.filter(iban=randiban):
                        break
                account = client.accounts_set.create(
                    iban=randiban,
                    currency_id=currency_id,
                    balance=0,
                    iz_freeze=False)
                account.save()
            else:
                account = Accounts.objects.get(iban=account_post)
            while True:
                randnumber = int(str(system_post) + "23814" + "%010d" % random.randint(0, 99_9999_9999))
                if not Cards.objects.filter(number=randnumber):
                    break
            card = Cards.objects.create(
                number=randnumber,
                client=client,
                account=account,
                cardholder_name=cardholder_name,
                expiration_date=datetime.date(year=datetime.datetime.now().year + time_post,
                                              month=datetime.datetime.now().month,
                                              day=31),
                security_code=random.randint(1, 999),
                iz_freeze=False)
            card.save()
            return redirect('/')

    return render(request, "new_card.html", {'form': card_form})


# Операция с выбранной картой
def card_page(request, number):
    if request.user.is_authenticated and not request.user.is_staff:
        client = Clients.objects.get(user=request.user.id)
        if client in Clients.objects.filter(cards__number=number):
            card = Cards.objects.get(number=number)
            templates = Templates.objects.all()
            return render(request, "card_page.html", {'card': card, 'templates': templates})

    return redirect('/')


def card_operation(request, number, template_id):
    if request.user.is_authenticated and not request.user.is_staff:
        client = Clients.objects.get(user=request.user.id)
        if client in Clients.objects.filter(cards__number=number):
            card = Cards.objects.get(number=number)
            template_filter = Templates.objects.filter(id=template_id)
            if template_filter:
                template = template_filter[0]

                if request.method == "POST":
                    card_number = request.POST.get("card_number")
                    print(card_number)
                    if not card_number:
                        iban = request.POST.get("iban")
                        print(iban)
                    value = request.POST.get("value")
                    print(value)

                else:
                    return render(request, "card_operation.html", {'card': card, 'template': template})

    return redirect('/')


def card_refill(request, number):
    if request.user.is_authenticated and not request.user.is_staff:
        client = get_object_or_404(Clients, user=request.user.id)
        card = get_object_or_404(Cards, pk=number, client=client)
        if request.method == "POST":
            value = int(request.POST.get("value"))
            account = card.account
            account.balance += value
            account.save()
            redirect(f'/cards/{number}/')
        else:
            return render(request, "card_refill.html", {'card': card})

    return redirect('/')
