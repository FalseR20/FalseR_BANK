import datetime
import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .models import *
from .forms import *
from .bank_functions import *


# Главная страница
def index(request):
    if not request.user.is_authenticated:
        return render(request, "guest.html")

    if request.user.is_staff:
        return render(request, "base.html", {"staff_user": request.user})

    client = Clients.objects.get(user=request.user.id)
    cards = Cards.objects.filter(client=client)
    accounts = Accounts.objects.filter(clients=client)
    return render(request, "index.html", {"client": client,
                                          "cards": cards,
                                          "accounts": accounts})


# Регистрация
def sign_up(request):
    if request.method == "GET":
        user_form = UserRegistration()
        return render(request, "registration/signup.html", {"form": user_form})

    user_form = UserRegistration(request.POST)
    username = request.POST.get("username")
    password = request.POST.get("password")
    confirm_password = request.POST.get("confirm_password")

    if not user_form.is_valid() or password != confirm_password \
            or User.objects.filter(username=username).first():
        return render(request, "registration/signup.html", {"form": user_form})

    user = User(username=username)
    user.set_password(password)  # с хешированием
    user.save()

    fullname = request.POST.get("fullname")
    client = Clients(fullname=fullname)
    client.user = user
    client.save()
    login(request, user)
    return redirect("/")


# Вход
def sign_out(request):
    logout(request)
    return redirect("/")


# Добавление карты
@login_required
def new_card(request):
    client = get_object_or_404(Clients, user=request.user.id)
    accounts = (tuple((account.iban, f"{account.iban} ({account.currency.code})") for account in
                      Accounts.objects.filter(clients=client)) +
                tuple((str(-currency.id), f"New account in {currency.code}") for currency in Currencies.objects.all()))
    card_form = CardForm(account_choices=accounts, cardholder_name=client.fullname.upper())

    if request.method == "GET":
        return render(request, "new_card.html", {'form': card_form})

    system_post = int(request.POST.get("system"))
    time_post = int(request.POST.get("time"))
    cardholder_name = request.POST.get("cardholder_name").upper()
    account_post = request.POST.get("account")

    # card_form = CardForm(request.POST, cardholder_name=cardholder_name)
    # if not card_form.is_valid():
    #     return render(request, "new_card.html", {'form': card_form})

    if account_post[0] == '-':
        currency_id = -int(account_post)
        while True:
            random_iban = make_iban("1" + Currencies.objects.get(id=currency_id).code,
                                    f"{random.randint(0, 9999_9999_9999_9999): 016d}")
            if not Accounts.objects.filter(iban=random_iban).first():
                break
        account = client.accounts_set.create(iban=random_iban, currency_id=currency_id, balance=0, is_freeze=False)
        account.save()
    else:
        account = Accounts.objects.get(iban=account_post)
    while True:
        random_number = make_card(f"{system_post: 1d}23814{random.randint(0, 9_9999_9999): 09d}")
        if not Cards.objects.filter(number=random_number):
            break
    card = Cards.objects.create(
        number=random_number,
        client=client,
        account=account,
        cardholder_name=cardholder_name,
        expiration_date=datetime.date(year=datetime.datetime.now().year + time_post,
                                      month=datetime.datetime.now().month,
                                      day=31),
        security_code=random.randint(1, 999),
        is_freeze=False)
    card.save()
    return redirect('/')


# Страница карты
@login_required
def card_page(request, number):
    client = get_object_or_404(Clients, user=request.user.id)
    card = get_object_or_404(Cards, number=number, client=client)
    return render(request, "card_page.html", {'card': card,
                                              'templates_receive': Templates.objects.filter(is_send=False),
                                              'templates_send': Templates.objects.filter(is_send=True)})


@login_required()
def card_operation(request, number, template_id):
    client = get_object_or_404(Clients, user=request.user.id)
    card = get_object_or_404(Cards, number=number, client=client)
    template = get_object_or_404(Templates, id=template_id)

    if request.method == "GET":
        return render(request, "card_operation.html", {'card': card, 'template': template})

    value = int(request.POST.get("value"))
    account = card.account
    if template.is_need_card:
        other_card_number = request.POST.get("card_number")
    elif template.is_need_iban:
        other_iban = request.POST.get("iban")

    if template.is_send:
        pass
    else:
        account.balance += value
        account.save()
    return redirect(f'/cards/{number}/')
