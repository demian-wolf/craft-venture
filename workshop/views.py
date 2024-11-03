from django.views import View
from django.http import Http404
from django.shortcuts import render

from .models import Workshop


class WorkshopView(View):
    def get(self, request, id: int):
        try:
            workshop = Workshop.objects.get(id=id)
        except Workshop.DoesNotExist:
            raise Http404

        return render(
            request, "details_independent.html",
            {"workshop": workshop},
        )
