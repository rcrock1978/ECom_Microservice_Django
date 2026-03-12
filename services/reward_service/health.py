from django.http import JsonResponse


def health_check(_: object) -> JsonResponse:
    return JsonResponse({"service": "reward-service", "status": "ok"})
