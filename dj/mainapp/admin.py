from django.contrib import admin
from .models import *


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('user', 'fullname')


@admin.register(Currencies)
class CurrenciesAdmin(admin.ModelAdmin):
    list_display = ('code',)


@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('currency', 'course_buy', 'course_sale', 'change_time')


@admin.register(Accounts)
class AccountsAdmin(admin.ModelAdmin):
    list_display = ('iban', 'currency', 'balance', 'balance_freeze')


@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    list_display = ('number', 'client', 'account', 'cardholder_name', 'expiration_date', 'is_freeze')


@admin.register(Templates)
class TemplatesAdmin(admin.ModelAdmin):
    list_display = ('description', 'other_iban', 'info_label')


@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('template', 'sender_iban', 'receiver_iban',
                    'currency', 'value', 'commission', 'info', 'timestamp', 'is_successful')
