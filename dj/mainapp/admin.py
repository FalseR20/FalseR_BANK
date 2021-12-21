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
    list_display = ('iban', 'currency', 'balance', 'is_freeze')


@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    list_display = ('number', 'client', 'account', 'cardholder_name', 'expiration_date', 'display_code', 'is_freeze')

    def display_code(self, obj):
        return "***"

    display_code.short_description = 'security_code'


@admin.register(Templates)
class TemplatesAdmin(admin.ModelAdmin):
    list_display = ('description', 'other_iban', 'is_need_iban', 'is_need_card', 'label')


@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('template', 'sender_iban', 'sender_card', 'receiver_iban', 'receiver_card',
                    'currency', 'value', 'commission', 'note', 'timestamp', 'is_successful')
