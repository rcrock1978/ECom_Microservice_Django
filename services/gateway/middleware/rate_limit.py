from django.utils.deprecation import MiddlewareMixin


class RateLimitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # placeholder implementation; integrate Redis or in-memory counters
        pass
