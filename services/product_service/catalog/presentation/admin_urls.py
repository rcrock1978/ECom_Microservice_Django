from django.urls import path

urlpatterns = [
    path("products/", lambda request: None),
    path("products/<str:slug>/", lambda request, slug: None),
    path("categories/", lambda request: None),
    path("categories/<str:slug>/", lambda request, slug: None),
]
