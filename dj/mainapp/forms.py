from django import forms


class UserRegistration(forms.Form):
    username = forms.CharField(label="Login", required=True)
    first_name = forms.CharField(label="Fullname", required=False)
    password = forms.CharField(widget=forms.PasswordInput, label="Password", required=True, min_length=4)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm password", required=True, min_length=4)

