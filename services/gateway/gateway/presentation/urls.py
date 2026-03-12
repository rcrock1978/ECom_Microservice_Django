from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.urls import path


def api_health(_: HttpRequest) -> JsonResponse:
    return JsonResponse({"service": "gateway", "status": "ok"})


def api_v1_docs(_: HttpRequest) -> HttpResponseRedirect:
    return HttpResponseRedirect("/api/docs/")


def api_v1_fallback(_: HttpRequest, path: str) -> JsonResponse:
    return JsonResponse({"detail": "Gateway route not implemented", "path": path}, status=404)

urlpatterns = [
    path("api/health/", api_health),
    path("api/v1/docs", api_v1_docs),
    path("api/v1/docs/", api_v1_docs),
    path("api/v1/<path:path>", api_v1_fallback),
]
