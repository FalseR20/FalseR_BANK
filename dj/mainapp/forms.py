from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegistrationForm(forms.Form):
    username = forms.SlugField(label="Login", max_length=150, required=True)
    fullname = forms.CharField(label="Fullname", max_length=30, required=True)
    password = forms.CharField(label="Password", max_length=128, required=True,
                               widget=forms.PasswordInput, min_length=4)
    confirm_password = forms.CharField(label="Confirm password", max_length=128, required=True,
                                       widget=forms.PasswordInput, min_length=4)

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        if User.objects.filter(username=username).first():
            message = f"User with name {username} already exists"
            raise ValidationError({'username': message})

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            message = "Passwords are not the same"
            raise ValidationError({'password': message, 'confirm_password': message})


class CardForm(forms.Form):
    system = forms.ChoiceField(label="System", choices=((4, "Visa"), (5, "Mastercard")))  # , (9, "БЕЛКАРТ")
    time = forms.ChoiceField(label="Service time",
                             choices=((1, "1 year"), (2, "2 years"), (3, "3 years"), (4, "4 years"), (5, "5 years")),
                             initial=4)

    def __init__(self, account_choices, cardholder_name, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs)
        self.fields['cardholder_name'] = forms.CharField(label="Cardholder name", initial=cardholder_name,
                                                         max_length=30)
        self.fields['account'] = forms.ChoiceField(label="Account", choices=account_choices)
