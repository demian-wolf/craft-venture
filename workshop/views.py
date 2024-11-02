from django.shortcuts import render, redirect

from .forms import SearchForm


def index(request):
    form = SearchForm(request.GET or None)

    if form.is_valid():
        return redirect("search", **form.cleaned_data)

    return render(
        request, "workshop/index.html",
        {"form": form},
    )


def search(request):
    form = SearchForm(request.GET or None)

    return render(request)
