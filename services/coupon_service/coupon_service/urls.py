from django.http import JsonResponse
from django.urls import path


def health(_: object) -> JsonResponse:
    return JsonResponse({"service": "coupon-service", "status": "ok"})


urlpatterns = [path("health/", health)]
