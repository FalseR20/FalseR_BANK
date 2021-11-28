from django import forms


class UserRegistration(forms.Form):
    username = forms.CharField(label="Login", required=True)
    fullname = forms.CharField(label="Fullname", required=False)
    password = forms.CharField(widget=forms.PasswordInput, label="Password", min_length=4, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm password",
                                       min_length=4, required=True)
