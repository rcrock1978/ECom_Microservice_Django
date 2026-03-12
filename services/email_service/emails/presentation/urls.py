from django.urls import path

urlpatterns = [
    path("admin/overview/", lambda request: None),
    path("admin/failed/", lambda request: None),
    path("admin/replay/", lambda request: None),
]
