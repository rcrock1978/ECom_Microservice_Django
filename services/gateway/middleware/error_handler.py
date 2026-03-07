from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse


class ErrorNormalizationMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        # return a normalized JSON error
        return JsonResponse({
            "error": str(exception),
        }, status=500)
