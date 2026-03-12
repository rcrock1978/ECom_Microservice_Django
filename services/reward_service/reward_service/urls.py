from django.http import JsonResponse
from django.urls import include, path


def health(_: object) -> JsonResponse:
    return JsonResponse({"service": "reward-service", "status": "ok"})


urlpatterns = [
    path("health/", health),
    path("api/v1/rewards/", include("rewards.presentation.urls")),
]
