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
    course_buy = models.BigIntegerField()  # (CUR / BYN * 1 000 000)
    course_sale = models.BigIntegerField()  # (CUR / BYN * 1 000 000)
    change_time = models.TimeField()


# 4. Счета клиентов в разных валютах
class Accounts(models.Model):
    iban = models.CharField(max_length=28, primary_key=True)
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=21, decimal_places=6)
    is_freeze = models.BooleanField()
    clients = models.ManyToManyField(Clients)

    def __str__(self):
        return self.iban


# 5. Карты клиентов
class Cards(models.Model):
    number = models.BigIntegerField(primary_key=True)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    cardholder_name = models.CharField(max_length=30)
    expiration_date = models.DateField()
    security_code = models.IntegerField()
    is_freeze = models.BooleanField()

    def __str__(self):
        return self.number


# 6. Шаблоны операций
class Templates(models.Model):
    description = models.CharField(max_length=50)
    other_iban = models.CharField(max_length=34, null=True)
    is_need_iban = models.BooleanField(default=False)
    is_need_card = models.BooleanField(default=False)
    label = models.CharField(max_length=30, default="Note")

    def __str__(self):
        return self.description


# 7. Операции
class Transactions(models.Model):
    template = models.ForeignKey(Templates, on_delete=models.CASCADE)
    sender_iban = models.ForeignKey(Accounts, related_name="sender_iban", on_delete=models.CASCADE)
    sender_card = models.ForeignKey(Cards, related_name="sender_card", on_delete=models.CASCADE, null=True)
    receiver_iban = models.ForeignKey(Accounts, related_name="receiver_iban", on_delete=models.CASCADE)
    receiver_card = models.ForeignKey(Cards, related_name="receiver_card", on_delete=models.CASCADE, null=True)
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=21, decimal_places=6)
    commission = models.DecimalField(max_digits=21, decimal_places=6)
    note = models.CharField(max_length=50, default="")
    timestamp = models.TimeField()
    is_successful = models.BooleanField()
