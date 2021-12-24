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
        self.fields['cardholder_name'] = forms.CharField(label="Cardholder name", max_length=30,
                                                         initial=cardholder_name, widget=forms.TextInput(attrs={
                                                             "oninput": "this.value = this.value.toUpperCase()"}))
        self.fields['account'] = forms.ChoiceField(label="Account", choices=account_choices)


class OperationForm(forms.Form):
    def __init__(self, template, balance, *args, **kwargs):
        super(OperationForm, self).__init__(*args, **kwargs)

        if not template.other_iban:
            self.fields['iban'] = forms.CharField(label="IBAN", max_length=34, required=True)
        self.fields['value'] = forms.DecimalField(label=f"Before {balance}", max_value=balance, min_value=0,
                                                  decimal_places=2, required=True)
        self.fields['info'] = forms.CharField(label=template.info_label, max_length=50)
