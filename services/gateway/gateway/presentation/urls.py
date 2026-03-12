from django.http import HttpRequest, HttpResponseRedirect
from django.urls import path
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from gateway.presentation.views import GatewayFacade


_gateway_facade = GatewayFacade.in_memory()


@extend_schema(operation_id="gateway_api_health", responses={200: OpenApiTypes.OBJECT})
@api_view(["GET"])
def api_health(_: Request) -> Response:
    return Response(_gateway_facade.health(), status=200)


@extend_schema(operation_id="gateway_api_docs_alias", responses={200: OpenApiTypes.OBJECT})
@api_view(["GET"])
def api_v1_docs(_: Request) -> Response:
    return Response({"docs_url": "/api/docs/", "schema_url": "/api/schema/", "redoc_url": "/api/redoc/"}, status=200)


def api_v1_docs_redirect(_: HttpRequest) -> HttpResponseRedirect:
    return HttpResponseRedirect("/api/docs/")


@extend_schema(
    operation_id="gateway_proxy_fallback",
    parameters=[OpenApiParameter(name="path", type=OpenApiTypes.STR, location=OpenApiParameter.PATH)],
    request=OpenApiTypes.OBJECT,
    responses={200: OpenApiTypes.OBJECT, 401: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT, 503: OpenApiTypes.OBJECT},
)
@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
def api_v1_fallback(request: Request, path: str) -> Response:
    access_token = ""
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        access_token = auth_header[7:]

    proxied = _gateway_facade.proxy(
        path=f"/api/v1/{path}",
        method=request.method,
        access_token=access_token or None,
    )
    return Response(proxied, status=int(proxied.get("status", 200)))

urlpatterns = [
    path("api/health/", api_health),
    path("api/v1/docs/redirect", api_v1_docs_redirect),
    path("api/v1/docs/", api_v1_docs),
    path("api/v1/docs", api_v1_docs),
    path("api/v1/<path:path>", api_v1_fallback),
]
