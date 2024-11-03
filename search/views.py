import math

from django.views import View
from django.db.models import F
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render, redirect

from search.models import TemporaryUser, UserSearch, UserSearchStage

from search.forms import SearchForm, UserSearchStageForm
from workshop.models import Workshop


class IndexView(View):
    def _get_ownership(self, request) -> dict:
        if request.user.is_authenticated:
            return {"user": request.user}
        
        temporary_user = TemporaryUser.objects.create()
        request.session["temporary_user_id"] = str(temporary_user.id)

        return {"temporary_user_id": temporary_user.id}

    def get(self, request):
        form = SearchForm()
        
        return render(
            request, "workshop/index.html", {"form": form},
        )
    
    def post(self, request):
        form = SearchForm(request.POST)

        if not form.is_valid():
            return render(
                request, "workshop/index.html", {"form": form},
            )

        ownership = self._get_ownership(request)

        # reset search for the user
        UserSearch.objects.filter(**ownership).delete()

        # create a new one
        UserSearch.objects.create(
            **ownership,
            starts_at=form.cleaned_data.get("starts_at"),
            ends_at=form.cleaned_data.get("ends_at"),
            radius=form.cleaned_data.get("radius"),
            lat=form.cleaned_data.get("lat"),
            lng=form.cleaned_data.get("lng"),
        )

        return redirect("search")


class UserSearchView(View):
    def _get_search(self, request):
        if request.user.is_authenticated:
            query = {"user": request.user}
        else:
            temporary_user_id = request.session.get("temporary_user_id")
            
            if not temporary_user_id:
                raise Http404

            try:
                temporary_user = TemporaryUser.objects.get(id=temporary_user_id)
            except TemporaryUser.DoesNotExist:
                raise Http404

            query = {"temporary_user": temporary_user}
        
        try:
            search = UserSearch.objects.get(**query)
        except UserSearch.DoesNotExist:
            raise Http404

        return search

    def _get_workshop(self, search, stages):
        used_workshop_ids = stages.values_list("workshop__id", flat=True)

        workshops = Workshop.objects.exclude(id__in=used_workshop_ids)
        workshops = iter(workshops)

        while True:
            w = next(workshops, None)

            if w is None:
                return None

            h = haversine(
                w.location.lng, w.location.lat,
                search.lng, search.lat,
            )

            if h <= search.radius:
                return w


    def get(self, request):
        search = self._get_search(request)

        stages = UserSearchStage.objects.filter(
            search=search,
            is_completed=True,
        )

        workshop = self._get_workshop(search, stages)

        if workshop is None:  # start over
            search.delete()
            return redirect("index")

        UserSearchStage.objects.get_or_create(
            search=search,
            workshop=workshop,
        )

        return render(
            request, "search/index.html", {"workshop": workshop},
        )

    def post(self, request):
        search = self._get_search(request)

        form = UserSearchStageForm(request.POST)

        if form.is_valid():
            is_accepted = form.cleaned_data.get("is_accepted")
            
            UserSearchStage.objects.update(
                search=search,
                is_completed=True,
                is_accepted=is_accepted,
            )

            return redirect("search")

        return render(
            request, "search/index.html", {"form": form},
        )



def haversine(lng1, lat1, lng2, lat2) -> float:
    R = 6371000

    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lng2 - lng1)

    a = math.sin(d_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(d_lambda / 2.0) ** 2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c
