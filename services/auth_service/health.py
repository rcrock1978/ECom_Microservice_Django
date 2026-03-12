from django.http import JsonResponse


def health_check(_: object) -> JsonResponse:
    return JsonResponse({"service": "auth-service", "status": "ok"})
