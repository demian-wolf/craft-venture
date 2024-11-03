from django.urls import path

from .views import WorkshopView

urlpatterns = [
    path('<int:id>', WorkshopView.as_view(), name="workshop-details"),
]
