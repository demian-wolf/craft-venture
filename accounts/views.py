from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView

from accounts.forms.sign_in_form import SignInForm
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


class SignInView(FormView):
    template_name = 'auth/sign_in.html'
    form_class = SignInForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=email, email=email, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid username or password!')
            return self.form_valid(form)


@login_required
def sign_out(request):
    logout(request)
    return redirect(reverse('index'))
