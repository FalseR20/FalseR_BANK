from django import forms


class UserRegistration(forms.Form):
    username = forms.CharField(label="Login", required=True)
    fullname = forms.CharField(label="Fullname", required=False)
    password = forms.CharField(widget=forms.PasswordInput, label="Password", min_length=4, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm password",
                                       min_length=4, required=True)


class CardForm(forms.Form):
    system = forms.ChoiceField(label="System", choices=((4, "Visa"), (5, "Mastercard"), (9, "БЕЛКАРТ")))
    time = forms.ChoiceField(label="Service time",
                             choices=((1, "1 year"), (2, "2 years"), (3, "3 years"), (4, "4 years"), (5, "5 years")),
                             initial=4)

    def __init__(self, account_choices, cardholder_name, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs)
        self.fields['cardholder_name'] = forms.CharField(label="Cardholder name", initial=cardholder_name,
                                                         max_length=30)
        self.fields['account'] = forms.ChoiceField(label="Account", choices=account_choices)
