from django.urls import path

urlpatterns = [
    path("api/v1/<path:path>", lambda request, path: None),
    path("api/health/", lambda request: None),
]
