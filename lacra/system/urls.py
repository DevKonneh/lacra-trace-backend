from django.urls import path

from lacra.system.views import HealthcheckView

urlpatterns = [
    path("healthcheck/", HealthcheckView.as_view(), name="system_healthcheck"),
]
