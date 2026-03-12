from django.urls import path

urlpatterns = [
    path("register/", lambda request: None),
    path("login/", lambda request: None),
    path("refresh/", lambda request: None),
    path("logout/", lambda request: None),
    path("me/", lambda request: None),
    path("forgot-password/", lambda request: None),
    path("reset-password/", lambda request: None),
]
