from django.views import View
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect

from workshop.models import Workshop
from search.models import TemporaryUser, UserSearch, SearchFeedback

from search.forms import SearchForm


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

        if request.user.is_authenticated:
            ownership = {"user": request.user}
        else:
            temporary_user = TemporaryUser.objects.create()
            request.session["temporary_user_id"] = str(temporary_user.id)

            ownership = {"temporary_user_id": temporary_user.id}

        # reset session
        UserSearch.objects.filter(**ownership).delete()

        UserSearch.objects.create(
            **ownership,
            start_date=form.cleaned_data.get("start_date"),
            end_date=form.cleaned_data.get("end_date"),
            radius=form.cleaned_data.get("radius"),
        )

        return redirect("search")


class UserSearchView(View):
    def get(self, request):
        if request.user.is_authenticated:
            feedback = SearchFeedback.objects.filter(
                user=request.user,
            )
        else:
            temporary_user_id = request.session.get("temporary_user_id")

            if not temporary_user_id:
                return redirect("index")
            
            feedback = SearchFeedback.objects.filter(
                search__temporary_user__id=temporary_user_id,
            )

        workshop = Workshop.objects.exclude(
            id__in={f.workshop_id for f in feedback}
        ).first()

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
