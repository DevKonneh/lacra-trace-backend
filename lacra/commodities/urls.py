from django.urls import path

from lacra.commodities.views import CommoditiesBalancesListView, CommoditiesGroupsListView, CommoditiesListView

urlpatterns = [
    path("", CommoditiesListView.as_view(), name="commodities_list"),
    path("groups/", CommoditiesGroupsListView.as_view(), name="commodities_groups_list"),
    path("balances/", CommoditiesBalancesListView.as_view(), name="commodities_balances_list"),
]
