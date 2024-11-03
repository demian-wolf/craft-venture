from django import forms
from django.utils.translation import gettext as _


class SignInForm(forms.Form):
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email address',
                'class': 'form-control pl-4'
            }
        )
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-control pl-5'
            }
        )
    )