from django.urls import path

urlpatterns = [
    path("cart/", lambda request: None),
    path("cart/items/", lambda request: None),
    path("cart/items/<str:item_id>/", lambda request, item_id: None),
    path("cart/coupon/", lambda request: None),
]
