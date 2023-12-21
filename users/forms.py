from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, \
    PasswordResetForm
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
    """Common ModelForm class for editing or changing User data"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'Name',
                  'last_name': 'Surname'}


class PwdChangeForm(PasswordChangeForm):
    """Just adds placeholders to common PasswordChangeForm. I love placeholders, they look stylish"""

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['placeholder'] = 'current password'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'new password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'new password confirmation'


class PwdResetForm(PasswordResetForm):
    """Just adds placeholders to common PasswordResetForm"""

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Input your Email'
