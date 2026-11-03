from django.contrib import admin
from django.urls import include, path

auth_urlpatterns = [
    path("auth/jwt/", include("lacra.auth.jwt.urls")),
    path("auth/otp/", include("lacra.auth.otp.urls")),
    path("auth/registration/", include("lacra.auth.registration.urls")),
    path("auth/social/", include("lacra.auth.social.urls")),
]

data_urlpatterns = [
    path("analytics/", include("lacra.analytics.urls")),
    path("commodities/", include("lacra.commodities.urls")),
    path("harvest-seasons/", include("lacra.harvest_seasons.urls")),
    path("system/", include("lacra.system.urls")),
    path("notifications/", include("lacra.notifications.urls")),
    path("transactions/", include("lacra.transactions.urls")),
    path("users/", include("lacra.users.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(auth_urlpatterns + data_urlpatterns)),
    # Test mode: the same data endpoints, isolated in the test_mode schema (see
    # lacra.common.middleware.TestModeMiddleware and lacra.common.db_router). Auth
    # is deliberately not mounted here - logging in always happens against public.
    # Namespaced so reverse("transactions_list") keeps resolving the normal route -
    # without a namespace, reusing the same names here would make it ambiguous.
    path("api/v1/test/", include((data_urlpatterns, "test_mode"), namespace="test_mode")),
]
