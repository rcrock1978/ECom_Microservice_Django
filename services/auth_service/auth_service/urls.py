from django.http import JsonResponse
from django.urls import include, path


def health(_: object) -> JsonResponse:
    return JsonResponse({"service": "auth-service", "status": "ok"})


urlpatterns = [
    path("health/", health),
    path("api/v1/auth/", include("auth.presentation.urls")),
]
