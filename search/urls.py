from django.urls import path

from .views import IndexView, UserSearchView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('search', UserSearchView.as_view(), name="search"),
]
