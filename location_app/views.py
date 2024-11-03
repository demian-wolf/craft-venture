from django.shortcuts import render
from django.views.generic import View


class MapView(View):
    template_name = 'location_app/index.html'

    def get(self, request):
       context = {}

       return render(request, self.template_name, context)
