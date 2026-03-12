from django.http import JsonResponse


def health_check(_: object) -> JsonResponse:
    return JsonResponse({"service": "cart-service", "status": "ok"})
