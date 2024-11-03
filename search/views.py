from django.views import View
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

    def get(self, request):
        search = self._get_search(request)

        stages = UserSearchStage.objects.filter(
            search=search,
            is_completed=True,
        )

        used_workshop_ids = stages.values_list("workshop__id", flat=True)
        workshop = Workshop.objects.exclude(id__in=used_workshop_ids).first()

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
