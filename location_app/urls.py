from django.urls import path

from location_app.views import MapView

urlpatterns = [
    path('', MapView.as_view(), name='map'),
]
