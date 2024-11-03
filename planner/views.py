from django.views import View
from django.shortcuts import render

from search.models import TemporaryUser, UserSearch, UserSearchStage
from workshop.models import Workshop


class FavoritesView(View):
    def get(self, request):
        try:
            search = UserSearch.objects.get(
                **self._get_ownership(request),
            )
        except UserSearch.DoesNotExist:
            favorites = []
        else:
            stages = UserSearchStage.objects.filter(
                search=search,
                is_completed=True,
                is_accepted=True,
            )
            
            favorites = Workshop.objects.filter(
                id__in={stage.workshop.id for stage in stages},
            ).all()
        
        return render(
            request, "planner/favorites.html", {"favorites": favorites},
        )

    def _get_ownership(self, request) -> dict:
        if request.user.is_authenticated:
            return {"user": request.user}
        
        temporary_user = TemporaryUser.objects.create()
        request.session["temporary_user_id"] = str(temporary_user.id)

        return {"temporary_user_id": temporary_user.id}
