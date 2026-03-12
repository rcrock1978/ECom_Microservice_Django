from django.urls import path

from catalog.presentation.views import (
    category_detail_view,
    list_categories_view,
    list_products_view,
    product_detail_view,
)

urlpatterns = [
    path("products/", list_products_view),
    path("products/<slug:slug>/", product_detail_view),
    path("categories/", list_categories_view),
    path("categories/<slug:slug>/", category_detail_view),
]
