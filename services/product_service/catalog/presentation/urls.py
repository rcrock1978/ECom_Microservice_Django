from django.urls import path

urlpatterns = [
    path("products/", lambda request: None),
    path("products/<slug:slug>/", lambda request, slug: None),
    path("categories/", lambda request: None),
    path("internal/products/<str:product_id>/", lambda request, product_id: None),
]
