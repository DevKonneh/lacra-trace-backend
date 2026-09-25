from django.contrib import admin
from django.urls import include, path

api_v1_urlpatterns = [
    path("analytics/", include("lacra.analytics.urls")),
    path("auth/jwt/", include("lacra.auth.jwt.urls")),
    path("auth/otp/", include("lacra.auth.otp.urls")),
    path("auth/registration/", include("lacra.auth.registration.urls")),
    path("auth/social/", include("lacra.auth.social.urls")),
    path("commodities/", include("lacra.commodities.urls")),
    path("system/", include("lacra.system.urls")),
    path("notifications/", include("lacra.notifications.urls")),
    path("transactions/", include("lacra.transactions.urls")),
    path("users/", include("lacra.users.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(api_v1_urlpatterns)),
]
