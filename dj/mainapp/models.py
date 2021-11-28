from django.db import models
from django.contrib.auth.models import User


# 0. User из "коробки" - Пользователи

# 1. Клиенты - one-to-one с User (User может и не быть)
class Clients(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    fullname = models.CharField(max_length=30)


# 2. Валюты
class Currencies(models.Model):
    code = models.CharField(max_length=3)


# 3. Курсы валют в разное время
class Courses(models.Model):
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE)
    course_buy = models.BigIntegerField()
    course_sale = models.BigIntegerField()
    change_time = models.TimeField()


# 4. Счета клиентов в разных валютах
class Accounts(models.Model):
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=21, decimal_places=6)
    clients = models.ManyToManyField(Clients)


# 5. Карты клиентов
class Cards(models.Model):
    number = models.BigIntegerField(primary_key=True)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    cardholder_name = models.CharField(max_length=30)
    expiration_date = models.DateField()
    security_code = models.IntegerField()


# 6. Шаблоны операций (#7)
class Templates(models.Model):
    description = models.CharField(max_length=64)


# 7. Операции
class Operations(models.Model):
    template = models.ForeignKey(Templates, on_delete=models.CASCADE)
    time = models.TimeField()
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=21, decimal_places=6)
    commission = models.DecimalField(max_digits=21, decimal_places=6)
    is_active = models.BooleanField()
