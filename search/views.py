from django.views import View
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect

from search.models import TemporaryUser, UserSearch, UserSearchStage

from search.forms import SearchForm
from workshop.models import Workshop


def _ownership(request) -> dict:
    if request.user.is_authenticated:
        return {"user": request.user}
    
    temporary_user = TemporaryUser.objects.create()
    request.session["temporary_user_id"] = str(temporary_user.id)

    return {"temporary_user_id": temporary_user.id}


class IndexView(View):
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

        ownership = _ownership(request)
        data = form.cleaned_data

        # reset search for the user
        UserSearch.objects.filter(**ownership).delete()

        # create a new one
        UserSearch.objects.create(
            **ownership,
            starts_at=data.get("starts_at"),
            ends_at=data.get("ends_at"),
            radius=data.get("radius"),
        )

        return redirect("search")


class UserSearchView(View):
    def get(self, request):
        if request.user.is_authenticated:
            search = UserSearch.objects.get(user=request.user)
        else:
            temporary_user_id = request.session.get("temporary_user_id")
            temporary_user = TemporaryUser.objects.get(id=temporary_user_id)

            search = UserSearch.objects.get(temporary_user=temporary_user)

        exclude = {stage.workshop.id for stage in UserSearchStage.objects.filter(
            search=search,
        )}

        exclude = UserSearchStage.objects.filter(
            search=search,
        ).values_list("workshop__id", flat=True)

        workshop = Workshop.objects.exclude(
            id__in=exclude,
        ).exclude(
            is_completed=True,
        ).first()

        UserSearchStage.objects.create(
            search=search,
            workshop=workshop,
        )

        return render(
            request, "search/index.html", {"workshop": workshop},
        )

    def post(self, request):
        workshop_id = request.POST.get("workshop_id")
        is_accepted = request.POST.get("accepted")
        
        if (workshop_id is None) or (is_accepted is None):
            raise HttpResponseBadRequest

        if request.user.is_authenticated:
            ownership = {"user": request.user}
        else:
            temporary_user_id = request.session.get("temporary_user_id")

            if temporary_user_id is None:
                raise Http404

            ownership = {"temporary_user_id": temporary_user_id}

        if is_accepted.lower() == "true":
            is_accepted = True
        elif is_accepted.lower() == "false":
            is_accepted = False
        else:
            return HttpResponseBadRequest("Invalid accepted status. Expected 'true' or 'false'.")

        feedback = SearchFeedback.objects.create(
            workshop_id=workshop_id,
            is_accepted=is_accepted,
            **ownership,
        )
        feedback.save()

        return HttpResponse("", status=204)
