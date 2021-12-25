from functools import partial
import random

from django.db import models
from django.contrib.auth.models import User


# 0. User из "коробки" - Пользователи

# 1. Клиенты - one-to-one с User (User может и не быть)
class Clients(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    fullname = models.CharField(max_length=30)

    def __str__(self):
        return self.fullname


# 2. Валюты
class Currencies(models.Model):
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.code


# 3. Курсы валют в разное время
class Courses(models.Model):
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE)
    course_buy = models.BigIntegerField()  # (BYN / CUR * 1 000 000)
    course_sale = models.BigIntegerField()  # (BYN / CUR * 1 000 000)
    change_time = models.TimeField(auto_now_add=True)


# 4. Счета клиентов в разных валютах
class Accounts(models.Model):
    iban = models.CharField(max_length=28, primary_key=True)
    clients = models.ManyToManyField(Clients)
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=21, decimal_places=6)
    balance_freeze = models.DecimalField(max_digits=21, decimal_places=6, default=0)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return self.iban


# 5. Карты клиентов
class Cards(models.Model):
    number = models.BigIntegerField(primary_key=True)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    cardholder_name = models.CharField(max_length=30)
    expiration_date = models.DateField()
    security_code = models.IntegerField(default=partial(random.randint, 1, 999))
    is_freeze = models.BooleanField(default=False)

    def __str__(self):
        return self.number


# 6. Шаблоны операций
class Templates(models.Model):
    description = models.CharField(max_length=50)
    other_iban = models.CharField(max_length=34)
    info_label = models.CharField(max_length=30, default="Note")
    commission_percent = models.DecimalField(max_digits=9, decimal_places=6, default=0)  # ***.****** %

    def __str__(self):
        return self.description


# 7. Операции
class Transactions(models.Model):
    template = models.ForeignKey(Templates, on_delete=models.CASCADE, null=True)
    sender_iban = models.CharField(max_length=34)
    receiver_iban = models.CharField(max_length=34)
    sender_card_number = models.BigIntegerField(null=True)
    receiver_card_number = models.BigIntegerField(null=True)
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=21, decimal_places=6)
    commission = models.DecimalField(max_digits=21, decimal_places=6, default=0)
    info = models.CharField(max_length=50)
    datetime = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=True)

    def __str__(self):
        return self.template.description
