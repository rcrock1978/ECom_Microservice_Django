from django.urls import path

urlpatterns = [
    path("validate/", lambda request: None),
    path("redeem/", lambda request: None),
    path("admin/coupons/", lambda request: None),
    path("admin/coupons/<str:code>/", lambda request, code: None),
]
