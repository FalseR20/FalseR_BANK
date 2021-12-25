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
        form = RegistrationForm()
        return render(request, "input_page.html", {"form": form, 'operation': "Registration",
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
    accounts_and_currencies = (tuple((account.iban, f"{account.iban} ({account.currency.code})") for account in
                                     Accounts.objects.filter(clients=client)) +
                               tuple((str(-currency.id), f"New account in {currency.code}") for currency in
                                     Currencies.objects.all()))
    form = NewCardForm(accounts_and_currencies, client.fullname.upper())

    if request.method == "GET":
        return render(request, "input_page.html", {"form": form,
                                                   'operation': "New card", 'button_value': "Create card"})

    form = NewCardForm(accounts_and_currencies, client.fullname.upper(), request.POST)
    if not form.is_valid():
        return render(request, "input_page.html", {"form": form,
                                                   'operation': "New card", 'button_value': "Create card"})

    system_post = int(form.cleaned_data["system"])
    time_post = int(form.cleaned_data["time"])
    cardholder_name = form.cleaned_data["cardholder_name"].upper()
    account_post = form.cleaned_data["account"]

    if account_post[0] == '-':
        currency_id = -int(account_post)
        while True:
            random_iban = make_iban("1" + Currencies.objects.get(id=currency_id).code,
                                    f"{random.randint(0, 9999_9999_9999_9999):016d}")
            if not Accounts.objects.filter(iban=random_iban).first():
                break
        account = client.accounts_set.create(iban=random_iban, currency_id=currency_id, balance=100)
    else:
        account = Accounts.objects.get(iban=account_post)
    while True:
        random_number = make_card(f"{system_post:1d}23814{random.randint(0, 9_9999_9999):09d}")
        if not Cards.objects.filter(number=random_number):
            break
    Cards.objects.create(
        number=random_number,
        client=client,
        account=account,
        cardholder_name=cardholder_name,
        expiration_date=datetime.date(year=datetime.datetime.now().year + time_post,
                                      month=datetime.datetime.now().month,
                                      day=31))
    return redirect('/')


# Страница карты
@login_required
def card_page(request, number):
    client = get_object_or_404(Clients, user=request.user.id)
    card = get_object_or_404(Cards, number=number, client=client)
    transactions = Transactions.objects.filter(
        Q(sender_card_number=card.number) |
        Q(receiver_card_number=card.number)
    )
    return render(request, "cards/main.html", {'card': card,
                                               'templates': Templates.objects.all(),
                                               'transactions': transactions,
                                               'user_iban': card.account.iban})


def sending(account, other_account, transaction, value):
    if not other_account:
        account.balance -= value
        account.save()
        print("not other_account")
    else:
        if other_account.is_closed:
            transaction.is_successful = False
        else:
            account.balance -= value
            account.save()

            if account.currency.id == other_account.currency.id:
                other_account.balance += value
            else:
                other_account.balance += (
                        value
                        * Courses.objects.filter(currency=account.currency).latest('change_time').course_sale
                        / Courses.objects.filter(currency=other_account.currency).latest('change_time').course_buy
                )
            other_account.save()


@login_required
def send_to_account(request, number):
    client = get_object_or_404(Clients, user=request.user.id)
    card = get_object_or_404(Cards, number=number, client=client)
    account = card.account
    balance = account.balance - account.balance_freeze
    form = AccountOperationForm(balance, account.currency.code, "Message")
    if request.method == "GET":
        return render(request, "input_page.html", {"form": form, 'operation': "Sending to account",
                                                   'button_value': "Send"})

    form = AccountOperationForm(balance, account.currency.code, "Message", request.POST)
    if not form.is_valid():
        return render(request, "input_page.html", {"form": form, 'operation': "Sending to account",
                                                   'button_value': "Send"})

    value = form.cleaned_data["value"]
    info = form.cleaned_data["info"]
    other_iban = form.cleaned_data["iban"]
    transaction = Transactions.objects.create(sender_iban=account.iban, sender_card_number=number,
                                              receiver_iban=other_iban,
                                              currency=account.currency, value=value, info=info)

    other_account = Accounts.objects.filter(iban=other_iban).first()
    sending(account, other_account, transaction, value)
    transaction.save()
    return redirect(f'/cards/{number}/')


@login_required
def send_to_card(request, number):
    client = get_object_or_404(Clients, user=request.user.id)
    card = get_object_or_404(Cards, number=number, client=client)
    account = card.account
    balance = account.balance - account.balance_freeze
    form = CardOperationForm(balance, account.currency.code, "Message")
    if request.method == "GET":
        return render(request, "input_page.html", {"form": form, 'operation': "Sending to card",
                                                   'button_value': "Send"})

    form = CardOperationForm(balance, account.currency.code, "Message", request.POST)
    if not form.is_valid():
        return render(request, "input_page.html", {"form": form, 'operation': "Sending to card",
                                                   'button_value': "Send"})

    value = Decimal(form.cleaned_data["value"])
    info = form.cleaned_data["info"]
    other_card = form.cleaned_data["card"]
    transaction = Transactions.objects.create(sender_iban=account.iban, sender_card_number=number,
                                              receiver_card_number=other_card,
                                              currency=account.currency, value=value, info=info)

    other_account = Accounts.objects.filter(cards__number=other_card).first()
    if other_account:
        transaction.receiver_iban = other_account.iban
        sending(account, other_account, transaction, value)
    transaction.save()
    return redirect(f'/cards/{number}/')


# Страница подтверждения операции
@login_required
def template_operation(request, number, template_id):
    client = get_object_or_404(Clients, user=request.user.id)
    card = get_object_or_404(Cards, number=number, client=client)
    account = card.account
    balance = account.balance - account.balance_freeze
    template = get_object_or_404(Templates, id=template_id)
    form = OperationForm(balance, account.currency.code, template.info_label)
    if request.method == "GET":
        return render(request, "input_page.html", {"form": form, 'operation': template.description,
                                                   'button_value': "Send"})

    form = OperationForm(balance, account.currency.code, template.info_label, request.POST)
    if not form.is_valid():
        return render(request, "input_page.html", {"form": form, 'operation': template.description,
                                                   'button_value': "Send"})

    value = Decimal(form.cleaned_data["value"])
    info = form.cleaned_data["info"]
    other_iban = template.other_iban
    transaction = Transactions.objects.create(sender_iban=account.iban, sender_card_number=number,
                                              receiver_iban=other_iban,
                                              currency=account.currency, value=value, info=info)

    other_account = Accounts.objects.filter(iban=other_iban).first()
    sending(account, other_account, transaction, value)
    transaction.save()
    return redirect(f'/cards/{number}/')


# Страничка с информацией о карте
@login_required
def card_info(request, number):
    client = get_object_or_404(Clients, user=request.user.id)
    card = get_object_or_404(Cards, number=number, client=client)
    account = card.account
    info_dict = {
        'Card number': card.number,
        'Cardholder name': card.cardholder_name,
        'Expiration date': card.expiration_date.strftime('%m/%y'),
        'Security code': card.security_code,
        'Card is freeze': card.is_freeze,
        '———': '———',
        'iban': account.iban,
        'Balance': f"{account.balance: .2f} {account.currency}",
        'Freeze balance': f"{account.balance_freeze: .2f} {account.currency}",
        'Account is closed': account.is_closed,
    }
    return render(request, "cards/info.html", {"info_dict": info_dict})


# Страничка с информацией о транзакции
@login_required
def card_info(request, number, transaction_id):
    client = get_object_or_404(Clients, user=request.user.id)
    card = get_object_or_404(Cards, number=number, client=client)
    if not card:
        return redirect('/')
    transaction = get_object_or_404(Transactions, id=transaction_id)
    template = transaction.template

    info_dict = {
        'id': transaction.id,
        "Description": template.description if template else "Sending by parameters",
        "Sender's iban": transaction.sender_iban,
        "Receiver's iban": transaction.receiver_iban,
        "Sender's card number": transaction.sender_card_number,
        "Receiver's card number": transaction.receiver_card_number,
        "Value": f"{transaction.value:.2f} {transaction.currency.code}",
        "Commission": f"{transaction.commission:.2f} {transaction.currency.code}",
        "Date and time": transaction.datetime,
        template.info_label if template else "Message": transaction.info,
        "Transaction is success": transaction.is_successful,


    }
    return render(request, "cards/info.html", {"info_dict": info_dict})
