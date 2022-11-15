from rest_framework.serializers import ModelSerializer

from . import models


class CurrenciesSerializer(ModelSerializer):
    class Meta:
        model = models.Currencies
        # fields = ("code",)
        fields = "__all__"


class ClientsSerializer(ModelSerializer):
    class Meta:
        model = models.Clients
        # fields = ("user", "fullname")
        fields = "__all__"


class CoursesSerializer(ModelSerializer):
    class Meta:
        model = models.Courses
        # fields = ("currency", "course_buy", "course_sale", "change_time")
        fields = "__all__"


class AccountsSerializer(ModelSerializer):
    class Meta:
        model = models.Accounts
        # fields = ("iban", "clients", "currency", "balance", "balance_freeze", "is_closed")
        fields = "__all__"


class CardsSerializer(ModelSerializer):
    class Meta:
        model = models.Cards
        # fields = ("number", "client", "account", "cardholder_name", "expiration_date", "security_code", "is_freeze")
        depth = 2
        fields = "__all__"


class TemplatesSerializer(ModelSerializer):
    class Meta:
        model = models.Templates
        # fields = ("description", "other_iban", "info_label", "commission_percent")
        fields = "__all__"


class TransactionsSerializer(ModelSerializer):
    class Meta:
        model = models.Transactions
        # fields = ("number", "client", "account", "cardholder_name", "expiration_date", "security_code", "is_freeze")
        fields = "__all__"
