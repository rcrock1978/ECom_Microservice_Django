from django.urls import path

from .views import (
    ProductListView,
    ProductDetailView,
    CategoryListView,
    InternalProductView,
)

urlpatterns = [
    path('products/', ProductListView.as_view()),
    path('products/<slug:slug>/', ProductDetailView.as_view()),
    path('categories/', CategoryListView.as_view()),
    path('internal/products/<int:pk>/', InternalProductView.as_view()),
]
