from decimal import Decimal
import datetime
import random

from django.contrib.auth.decorators import login_required
from django.db.models import Q
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
        return render(request, "input_page.html", {"form": RegistrationForm(), 'operation': "Registration",
                                                   'button_value': "Sign up", 'is_need_agreement': True})

    form = RegistrationForm(request.POST)
    if not form.is_valid():
        return render(request, "input_page.html", {"form": form, 'operation': "Registration",
                                                   'button_value': "Sign up", 'is_need_agreement': True})

    username = form.cleaned_data["username"]
    fullname = form.cleaned_data["fullname"]
    password = form.cleaned_data["password"]

    user = User(username=username)
    user.set_password(password)  # с хешированием
    user.save()
    Clients.objects.create(fullname=fullname, user=user)
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
        return render(request, "cards/new.html", {'form': card_form})

    system_post = int(request.POST.get("system"))
    time_post = int(request.POST.get("time"))
    cardholder_name = request.POST.get("cardholder_name").upper()
    account_post = request.POST.get("account")

    if account_post[0] == '-':
        currency_id = -int(account_post)
        while True:
            print("1" + Currencies.objects.get(id=currency_id).code, f"{random.randint(0, 9999_9999_9999_9999):016d}",
                  sep='\n')
            random_iban = make_iban("1" + Currencies.objects.get(id=currency_id).code,
                                    f"{random.randint(0, 9999_9999_9999_9999):016d}")
            if not Accounts.objects.filter(iban=random_iban).first():
                break
        account = client.accounts_set.create(iban=random_iban, currency_id=currency_id, balance=100)
        account.save()
    else:
        account = Accounts.objects.get(iban=account_post)
    while True:
        random_number = make_card(f"{system_post:1d}23814{random.randint(0, 9_9999_9999):09d}")
        if not Cards.objects.filter(number=random_number):
            break
    card = Cards.objects.create(
        number=random_number,
        client=client,
        account=account,
        cardholder_name=cardholder_name,
        expiration_date=datetime.date(year=datetime.datetime.now().year + time_post,
                                      month=datetime.datetime.now().month,
                                      day=31))
    card.save()
    return redirect('/')


# Страница карты
@login_required
def card_page(request, number):
    client = get_object_or_404(Clients, user=request.user.id)
    card = get_object_or_404(Cards, number=number, client=client)
    transactions = Transactions.objects.filter(
        Q(sender_iban=card.account.iban) |
        Q(receiver_iban=card.account.iban)
    )
    return render(request, "cards/main.html", {'card': card,
                                               'templates': Templates.objects.all(),
                                               'transactions': transactions,
                                               'user_iban': card.account.iban})


# Страница подтверждения операции
@login_required
def card_operation(request, number, template_id):
    client = get_object_or_404(Clients, user=request.user.id)
    card = get_object_or_404(Cards, number=number, client=client)
    template = get_object_or_404(Templates, id=template_id)
    if request.method == "GET":
        return render(request, "cards/operations.html", {'card': card, 'template': template})

    account = card.account
    value = Decimal(request.POST.get("value"))
    if value > account.balance - account.balance_freeze:
        return render(request, "cards/operations.html", {'card': card, 'template': template})
    account.balance -= value
    account.save()
    info = request.POST.get("info")
    other_iban = template.other_iban
    if not other_iban:
        other_iban = request.POST.get("iban")

    transaction = Transactions.objects.create(template=template, sender_iban=account.iban, receiver_iban=other_iban,
                                              currency=account.currency, value=value, info=info)
    transaction.save()

    other_account = Accounts.objects.filter(iban=other_iban).first()
    if other_account:
        if account.currency == other_account.currency:
            other_account.balance += value
        else:
            other_account.balance += (
                    value
                    * Courses.objects.filter(currency=account.currency.id).latest('change_time').course_sale
                    / Courses.objects.filter(currency=other_account.currency.id).latest('change_time').course_buy
            )
        other_account.save()
    return redirect(f'/cards/{number}/')


# Страничка с информацией о карте
@login_required
def info(request, number):
    client = get_object_or_404(Clients, user=request.user.id)
    card = get_object_or_404(Cards, number=number, client=client)
    account = card.account
    info_dict = {
        'number': card.number,
        'cardholder_name': card.cardholder_name,
        'expiration_date': card.expiration_date.strftime('%m/%y'),
        'security_code': card.security_code,
        '———': '———',
        'iban': account.iban,
        'balance': f"{account.balance: .2f} {account.currency}",
    }
    return render(request, "cards/info.html", {"info_dict": info_dict})
