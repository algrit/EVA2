from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserRegisterForm(UserCreationForm):
    """This form inherits fields from base class, but adds placeholder attr"""

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'placeholder': 'username', 'data-bs-toggle': 'tooltip',
             'title': 'Test tooltip. Will be changed later. Now default Django constraints'})
        self.fields['password1'].widget.attrs['placeholder'] = 'password'
        self.fields['password2'].widget.attrs['placeholder'] = 'password confirmation'

    class Meta:
        model = User
        fields = ['username']


class ModalLoginForm(AuthenticationForm):
    """This form used in Login Modal Window of Navbar.
    Inherits all methods of Base class, but I wanted to rewrite fields. Dunno, just for fun:)"""
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True,
                                                           'placeholder': 'username'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password",
                                          'placeholder': 'password'}),
    )


class AccountSettings(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'Name',
                  'last_name': 'Surname'}