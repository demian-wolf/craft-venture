from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView, View

from accounts.forms.sign_up_form import SignUpForm


class SignUpView(FormView):
    form_class = SignUpForm
    template_name = 'auth/sign_up.html'

    def form_valid(self, form):
        try:
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                raise ValidationError('Passwords must match')

            user = User.objects.create_user(username=email,
                                            email=email,
                                            password=password)
            user.save()
            return HttpResponse('<h1>Good!</h1>')
        except:
            form.add_error(None, 'Invalid email or password!')
            return self.form_invalid(form)


class SignInView(View):
    pass

# Create your views here.
