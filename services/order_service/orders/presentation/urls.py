from django.urls import path

urlpatterns = [
    path("", lambda request: None),
    path("<str:order_number>/", lambda request, order_number: None),
    path("<str:order_number>/cancel/", lambda request, order_number: None),
    path("webhook/payment/", lambda request: None),
    path("admin/<str:order_number>/status/", lambda request, order_number: None),
]
