from rest_framework import serializers

from .models import Currencies


class CurrenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currencies
        fields = ("code",)
