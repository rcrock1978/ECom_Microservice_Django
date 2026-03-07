from django.utils.deprecation import MiddlewareMixin
from ..application.jwt_utils import verify_token


class GatewayAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
            try:
                payload = verify_token(token)
                request.user_payload = payload
            except Exception:
                request.user_payload = None
        else:
            request.user_payload = None
