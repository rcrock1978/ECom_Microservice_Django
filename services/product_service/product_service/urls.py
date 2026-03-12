from django.http import JsonResponse
from django.urls import include, path


def health(_: object) -> JsonResponse:
    return JsonResponse({"service": "product-service", "status": "ok"})


urlpatterns = [
    path("health/", health),
    path("api/v1/", include("catalog.presentation.urls")),
    path("api/v1/admin/catalog/", include("catalog.presentation.admin_urls")),
]
