from django.http import JsonResponse
from django.urls import include, path


def health(_: object) -> JsonResponse:
    return JsonResponse({"service": "gateway", "status": "ok"})


urlpatterns = [path("health/", health)]
urlpatterns += [
    path("", include("gateway.presentation.urls")),
]
