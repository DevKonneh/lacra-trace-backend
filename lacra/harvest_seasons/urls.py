from django.urls import path

from lacra.harvest_seasons.views import HarvestSeasonsListView

urlpatterns = [
    path("", HarvestSeasonsListView.as_view(), name="harvest_seasons_list"),
]
