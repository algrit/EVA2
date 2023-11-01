from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation

class UserRegisterForm(UserCreationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          'placeholder': 'password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          'placeholder': 'repeat the password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        # widgets = {
        #     'username': forms.TextInput(attrs={'placeholder': 'username'}),
        #     'password1': forms.TextInput(attrs={'placeholder': 'TEST'}),
        #     'password2': forms.PasswordInput(attrs={'placeholder': 'TEST'}),
        # }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)
