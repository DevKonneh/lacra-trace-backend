from typing import Any

from rest_framework import views
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from lacra.auth.registration.schemas.requests import RegistrationRequest
from lacra.auth.registration.schemas.responses import RegisteredResponse
from lacra.auth.registration.services import RegistrationService
from lacra.common.throttling import AuthThrottle


class RegistrationView(views.APIView):
    permission_classes = (AllowAny,)
    throttle_classes = [AuthThrottle]

    def post(self, request: Request, *_: Any, **__: Any) -> Response:
        payload = RegistrationRequest.parse(request)
        RegistrationService.register(payload)
        return RegisteredResponse().as_response()
