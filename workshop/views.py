
from django.shortcuts import render


def index(request):
    return render(request, "auth/sign_up.html")
