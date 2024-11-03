
from django.shortcuts import render


def index(request):
    return render(request, "auth/sign_up.html")


def signup(request):
    return render(request, "auth/sign_up.html")


def signin(request):
    return render(request, "auth/sign_in.html")
